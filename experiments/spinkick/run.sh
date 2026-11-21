#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "${script_dir}/../.." && pwd)"
output_root="${project_dir}/MimicKit/output"

if [[ "${1:-}" != "--worker" ]]; then
    mkdir -p "${output_root}"
    # Serialize launches; the fixed service name also prevents duplicate workers.
    exec 9>"${output_root}/.spinkick.lock"
    if ! flock -n 9; then
        echo "A spinkick experiment is already running." >&2
        exit 1
    fi
    if systemctl --user is-active --quiet texttomotion-spinkick.service; then
        echo "A spinkick experiment is already running." >&2
        exit 1
    fi
    out_dir="$(mktemp -d "${output_root}/spinkick_$(date +%Y%m%d_%H%M%S)_XXXXXX")"
    # A transient user service survives SSH disconnection and the launching terminal.
    systemd-run --user --unit=texttomotion-spinkick --collect --service-type=exec \
        --property="StandardOutput=append:${out_dir}/console.log" \
        --property=StandardError=inherit \
        /usr/bin/bash "${script_dir}/run.sh" --worker "${out_dir}"
    worker_pid="$(systemctl --user show texttomotion-spinkick.service --property=MainPID --value)"
    printf '%s\n' "${worker_pid}" >"${out_dir}/worker.pid"
    printf 'Started worker PID: %s\nOutput: %s\n' "${worker_pid}" "${out_dir}"
    exit 0
fi

out_dir="${2:?Missing output directory}"
trap 'result=$?; if (( result == 0 )); then printf "completed\n"; else printf "failed (exit %s)\n" "$result"; fi >"${out_dir}/status.txt"' EXIT
printf 'running\n' >"${out_dir}/status.txt"

source /home/jong/isaaclab/activate.sh
cd "${project_dir}/MimicKit"

num_envs=1024
milestones=(100 500 2000 5000)
steps_per_iter="$(python -c 'import yaml; print(yaml.safe_load(open("data/agents/deepmimic_humanoid_ppo_agent.yaml"))["steps_per_iter"])')"
[[ "${steps_per_iter}" =~ ^[1-9][0-9]*$ ]]
max_samples=$((5000 * num_envs * steps_per_iter))

{
    printf 'completed_iterations\ttraining_samples\tcheckpoint\n'
    for milestone in "${milestones[@]}"; do
        printf '%s\t%s\tmodel_%06d.pt\n' "${milestone}" "$((milestone * num_envs * steps_per_iter))" "${milestone}"
    done
} >"${out_dir}/milestones.tsv"

train_args=(
    --arg_file args/deepmimic_humanoid_ppo_args.txt
    --engine_config data/engines/isaac_lab_engine.yaml
    --mode train --num_envs "${num_envs}" --devices cuda:0
    --visualize false --video false --model_file ""
    --rand_seed 42 --logger txt --save_int_models false
    --checkpoint_iters "${milestones[@]}"
    --max_samples "${max_samples}" --out_dir "${out_dir}"
)
printf '%q ' python -u mimickit/run.py "${train_args[@]}" >"${out_dir}/command.txt"
printf '\n' >>"${out_dir}/command.txt"
printf 'Training from scratch: 1024 environments, checkpoints at 100/500/2000/5000 iterations.\n'
# A service stop sends SIGTERM to the worker and its training subprocess.
python -u mimickit/run.py "${train_args[@]}" &
train_pid=$!
printf '%s\n' "${train_pid}" >"${out_dir}/train.pid"
wait "${train_pid}"
