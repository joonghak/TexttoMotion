#!/home/jong/isaaclab/.venv/bin/python
"""Short training experiment: do direction, speed, action, and time really change the motion?

Usage on this computer:
    ./experiments/train_eval/run_experiment.py                    # 10 sentences, 500 iterations each (~100 min)
    ./experiments/train_eval/run_experiment.py --list             # sentence keys and groups
    ./experiments/train_eval/run_experiment.py --only base,left   # a subset
    ./experiments/train_eval/run_experiment.py --resume experiments/train_eval/<폴더>     # continue after a stop
    ./experiments/train_eval/run_experiment.py --play experiments/train_eval/<폴더> --group 방향
    ./experiments/train_eval/run_experiment.py --summarize experiments/train_eval/<폴더>

Every sentence changes one attribute of the baseline "앞으로 5초 걸어". For each sentence:
1. train_from_text.py --iters 500 parses it, builds the reference, and trains,
2. rollout_eval.py replays the policy once from the start of the clip (headless)
   and measures direction, speed, turning, foot height, and duration of the
   simulated character next to the same numbers of the reference.
report.md shows, per group, the target, the reference, and the measured motion with
an automatic O/X and an empty "눈 확인" column. The visual check is the main
judgement: --play opens the runs of a group one after another in the viewer.
About 10 minutes per sentence with 1024 environments on the RTX 5070.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

import play_motion  # noqa: E402
import train_from_text as tft  # noqa: E402

ROLLOUT_EVAL = HERE / "rollout_eval.py"
ITERS = 500
MINUTES_PER_SENTENCE = 10

# key, sentence, groups. Every sentence changes one thing of the baseline "base".
SENTENCES = [
    ("base", "앞으로 5초 걸어", ("방향", "속도", "시간", "동작")),
    ("left", "왼쪽으로 5초 걸어", ("방향",)),
    ("back", "뒤로 5초 걸어", ("방향",)),
    ("right", "오른쪽으로 5초 걸어", ("방향",)),
    ("slow", "천천히 앞으로 5초 걸어", ("속도",)),
    ("fast", "빠르게 앞으로 5초 걸어", ("속도",)),
    ("walk10", "앞으로 10초 걸어", ("시간",)),
    ("run", "앞으로 5초 달려", ("동작",)),
    ("kick", "앞으로 발차기 한 번 해", ("동작",)),
    ("spin", "스핀킥 한 번 해", ("동작",)),
]
GROUPS = {
    "방향": "같은 걷기에서 방향만 바꿈. 이동 방향이 0/90/180/270°로 달라져야 함.",
    "속도": "같은 걷기에서 속도만 바꿈. 실제 걷는 속도(m/s)가 달라져야 함.",
    "시간": "같은 걷기에서 길이만 바꿈. 지속 시간이 5초와 10초로 달라져야 함.",
    "동작": "기본값에서 동작만 바꿈. 이동 속도, 몸 회전, 발 높이가 동작마다 달라야 함.",
}
LOOK_FOR = {
    "방향": "캐릭터가 바닥 격자 기준으로 앞/왼쪽/뒤/오른쪽으로 걸어가는지",
    "속도": "천천히 < 보통 < 빠르게 순서로 걸음이 빨라지는지",
    "시간": "10초 걷기가 5초 걷기보다 두 배 길게 이어지는지",
    "동작": "걷기, 달리기(두 발이 뜸), 발차기, 스핀킥이 서로 다른 동작으로 보이는지",
}

# Automatic O/X tolerances; the visual check decides.
DIRECTION_TOL_DEG = 15.0
SPEED_TOL = 0.15          # relative: walking speed, spin turn rate
TURN_TOL_DEG = 60.0
FOOT_TOL_M = 0.25
COMPLETE = 0.98           # completion ratio counted as "did not fall before the end"


def selected(only):
    if not only:
        return SENTENCES
    keys = [key.strip() for key in only.split(",") if key.strip()]
    unknown = sorted(set(keys) - {key for key, _, _ in SENTENCES})
    if unknown:
        raise SystemExit(f"알 수 없는 키: {', '.join(unknown)} (--list로 확인)")
    return [sentence for sentence in SENTENCES if sentence[0] in keys]


def load(exp_dir: Path, key: str):
    run_dir = exp_dir / "runs" / key
    summary_file, eval_file = run_dir / "summary.json", run_dir / "eval.json"
    summary = json.loads(summary_file.read_text()) if summary_file.exists() else None
    evaluation = json.loads(eval_file.read_text()) if eval_file.exists() else None
    return run_dir, summary, evaluation


def is_trained(run_dir: Path) -> bool:
    summary_file = run_dir / "summary.json"
    return (summary_file.exists() and (run_dir / "train" / "model.pt").exists()
            and json.loads(summary_file.read_text())["training"]["status"] == "completed")


def run_sentence(exp_dir: Path, key: str, text: str, iters: int, num_envs: int) -> str:
    runs = exp_dir / "runs"
    run_dir = runs / key
    if not is_trained(run_dir):
        if run_dir.exists():
            stamp = datetime.datetime.now().strftime("%H%M%S")
            run_dir.rename(runs / f"{key}.incomplete-{stamp}")
        code = subprocess.run([sys.executable, str(ROOT / "train_from_text.py"), "--iters", str(iters),
                               "--num-envs", str(num_envs), "--out-root", str(runs), "--run-name", key,
                               text]).returncode
        if code == 130:
            raise KeyboardInterrupt
        if code != 0:
            return "파싱 거부" if code == 2 else f"학습 실패 (exit {code})"
    if not (run_dir / "eval.json").exists():
        code = tft.run_in_isaaclab([run_dir], log_file=run_dir / "eval_console.log", script=ROLLOUT_EVAL)
        if code != 0:
            return f"측정 실패 (exit {code})"
    return "완료"


def rel(path: Path) -> str:
    return os.path.relpath(path, ROOT)


def parsed_text(summary) -> str:
    return json.dumps(summary["parsed"], ensure_ascii=False) if summary else "-"


def fmt(value, unit="", digits=2):
    return "-" if value is None else f"{value:.{digits}f}{unit}"


def angle_error(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def completed(evaluation) -> bool:
    return bool(evaluation) and not evaluation["fell"] and evaluation["completion"] >= COMPLETE


def fall_note(evaluation) -> str:
    return "" if completed(evaluation) else f"넘어짐 {fmt(evaluation['fell_at_s'], '초', 1)}"


def verdict(evaluation, problems) -> str:
    if not evaluation:
        return "-"
    problems = [p for p in [fall_note(evaluation)] + problems if p]
    return "O" if not problems else "X (" + ", ".join(problems) + ")"


def spec_metric(action: str) -> tuple:
    """Speed measure per action: walking pace in m/s, spin tempo in deg/s."""
    return ("speed_mps", "m/s") if action in ("walk", "run") else ("turn_rate_dps", "°/s")


def group_table(group: str, rows) -> list:
    lines = [f"### {group}", "", GROUPS[group], ""]
    if group == "방향":
        lines += ["| 문장 | 목표 | 레퍼런스 이동 방향 | 실제 이동 방향 | 실제 시작 방향 | 판정 | 눈 확인 |",
                  "|---|---|---|---|---|---|---|"]
        for text, summary, ev in rows:
            target = 360.0 * summary["parsed"]["direction"] if summary else None
            sim, ref = (ev["sim"], ev["reference_window"]) if ev else ({}, {})
            problems = []
            if ev and angle_error(sim["travel_deg"], target) > DIRECTION_TOL_DEG:
                problems.append(f"방향 {angle_error(sim['travel_deg'], target):.0f}° 어긋남")
            lines.append(f"| {text} | {fmt(target, '°', 0)} | {fmt(ref.get('travel_deg'), '°', 0)} | "
                         f"{fmt(sim.get('travel_deg'), '°', 0)} | {fmt(sim.get('start_heading_deg'), '°', 0)} | "
                         f"{verdict(ev, problems)} | |")
    elif group == "속도":
        lines += ["| 문장 | 목표 속도(0~1) | 지표 | 레퍼런스 | 실제 | 판정 | 눈 확인 |", "|---|---|---|---|---|---|---|"]
        walk_speeds = []
        for text, summary, ev in rows:
            if not summary:
                lines.append(f"| {text} | - | - | - | - | - | |")
                continue
            metric, unit = spec_metric(summary["parsed"]["action"])
            sim = ev["sim"].get(metric) if ev else None
            ref = ev["reference_window"].get(metric) if ev else None
            problems = []
            if ev and ref and abs(sim - ref) > SPEED_TOL * ref:
                problems.append(f"레퍼런스 대비 {sim / ref - 1:+.0%}")
            if metric == "speed_mps" and sim is not None:
                walk_speeds.append((summary["parsed"]["speed"], sim))
            lines.append(f"| {text} | {summary['parsed']['speed']:g} | {unit} | {fmt(ref)} | {fmt(sim)} | "
                         f"{verdict(ev, problems)} | |")
        if len(walk_speeds) > 1:
            ordered = [speed for _, speed in sorted(walk_speeds)]
            lines += ["", "걷기 실제 속도가 목표 순서대로 커지는가: "
                      + ("O" if all(a < b for a, b in zip(ordered, ordered[1:])) else "X")
                      + " (" + " < ".join(f"{speed:.2f}" for speed in ordered) + " m/s)"]
    elif group == "시간":
        lines += ["| 문장 | 목표 시간 | 레퍼런스 길이 | 실제 지속 시간 | 스핀 횟수 (레퍼런스 / 실제) | 판정 | 눈 확인 |",
                  "|---|---|---|---|---|---|---|"]
        for text, summary, ev in rows:
            target = summary["parsed"]["duration"] if summary else None
            spins, problems = "-", []
            if ev and summary["parsed"]["action"] == "spinkick":
                ref_spins = abs(ev["reference_window"]["total_turn_deg"]) / 360.0
                sim_spins = abs(ev["sim"]["total_turn_deg"]) / 360.0
                spins = f"{ref_spins:.1f} / {sim_spins:.1f}"
                if abs(sim_spins - ref_spins) * 360.0 > TURN_TOL_DEG:
                    problems.append("회전 수 다름")
            lines.append(f"| {text} | {fmt(target, '초', 1)} | {fmt(ev and ev['reference_duration_s'], '초')} | "
                         f"{fmt(ev and ev['sim']['duration_s'], '초')} | {spins} | {verdict(ev, problems)} | |")
    elif group == "동작":
        lines += ["| 문장 | 동작 | 이동 속도 (레퍼런스 / 실제) | 몸 회전 | 최대 발 높이 | 발차기 횟수 | 판정 | 눈 확인 |",
                  "|---|---|---|---|---|---|---|---|"]
        for text, summary, ev in rows:
            action = summary["parsed"]["action"] if summary else "-"
            if not ev:
                lines.append(f"| {text} | {action} | - | - | - | - | - | |")
                continue
            sim, ref = ev["sim"], ev["reference_window"]
            problems = []
            if abs(sim["speed_mps"] - ref["speed_mps"]) > max(SPEED_TOL * ref["speed_mps"], 0.2):
                problems.append("속도")
            if abs(sim["total_turn_deg"] - ref["total_turn_deg"]) > TURN_TOL_DEG:
                problems.append("회전")
            if abs(sim["max_foot_height_m"] - ref["max_foot_height_m"]) > FOOT_TOL_M:
                problems.append("발 높이")
            lines.append(f"| {text} | {action} | {ref['speed_mps']:.2f} / {sim['speed_mps']:.2f} m/s | "
                         f"{ref['total_turn_deg']:.0f}° / {sim['total_turn_deg']:.0f}° | "
                         f"{ref['max_foot_height_m']:.2f} / {sim['max_foot_height_m']:.2f} m | "
                         f"{ref['kick_count']} / {sim['kick_count']} | {verdict(ev, problems)} | |")
    else:
        lines += ["| 문장 | 파싱 결과 | 완주 | 이동 속도 | 몸 회전 | 판정 | 눈 확인 |", "|---|---|---|---|---|---|---|"]
        for text, summary, ev in rows:
            lines.append(f"| {text} | {parsed_text(summary)} | "
                         f"{fmt(ev and ev['completion'] * 100, '%', 0)} | {fmt(ev and ev['sim']['speed_mps'], ' m/s')} | "
                         f"{fmt(ev and ev['sim']['total_turn_deg'], '°', 0)} | {verdict(ev, [])} | |")
    return lines + [""]


def training_minutes(summary):
    training = (summary or {}).get("training", {})
    if not training.get("finished"):
        return None
    started = datetime.datetime.fromisoformat(training["started"])
    return (datetime.datetime.fromisoformat(training["finished"]) - started).total_seconds() / 60.0


def return_per_step(summary):
    final = (summary or {}).get("training", {}).get("final_log") or {}
    if final.get("Test_Episode_Length"):
        return final["Test_Return"] / final["Test_Episode_Length"]
    return None


def summarize(exp_dir: Path) -> Path:
    data = {key: load(exp_dir, key) for key, _, _ in SENTENCES}
    lines = [f"# 500회 학습 실험: 방향·속도·동작·시간이 실제로 달라지는가", "",
             f"- 폴더: {exp_dir}", "- 자동 판정(O/X)은 참고용입니다. 최종 판단은 눈 확인 칸에 적어 주세요.", "",
             "## 눈으로 확인하는 법", ""]
    for group in GROUPS:
        lines.append(f"- {group}: `./experiments/train_eval/run_experiment.py --play {rel(exp_dir)} "
                     f"--group {group}` → {LOOK_FOR[group]}")
    lines += ["", "창을 닫거나 Ctrl+C를 누르면 다음 문장으로 넘어갑니다. 옆에 보이는 초록 캐릭터가 레퍼런스입니다.", "",
              "## 그룹별 결과", ""]
    for group in GROUPS:
        rows = [(text, data[key][1], data[key][2]) for key, text, groups in SENTENCES if group in groups]
        lines += group_table(group, rows)
    lines += ["## 전체", "", "| 키 | 문장 | 파싱 결과 | 학습 | 학습 시간 | 스텝당 보상 | 완주 | 몸통 위치 오차 | 몸 전체 위치 오차 |",
              "|---|---|---|---|---|---|---|---|---|"]
    csv_rows = []
    for key, text, groups in SENTENCES:
        _, summary, ev = data[key]
        parsed = summary["parsed"] if summary else None
        status = summary["training"]["status"] if summary else "미실행"
        lines.append(f"| {key} | {text} | {parsed_text(summary)} | {status} | "
                     f"{fmt(training_minutes(summary), '분', 1)} | {fmt(return_per_step(summary))} | "
                     f"{fmt(ev and ev['completion'] * 100, '%', 0)} | {fmt(ev and ev['root_pos_err_m'], ' m')} | "
                     f"{fmt(ev and ev['body_pos_err_m'], ' m')} |")
        row = {"key": key, "text": text, "groups": "/".join(groups), "status": status,
               "train_minutes": training_minutes(summary), "return_per_step": return_per_step(summary)}
        row.update({f"parsed_{name}": value for name, value in (parsed or {}).items()})
        if ev:
            row.update({name: ev[name] for name in ("end", "fell", "fell_at_s", "completion", "reference_duration_s",
                                                   "root_pos_err_m", "body_pos_err_m")})
            row.update({f"sim_{name}": value for name, value in ev["sim"].items()})
            row.update({f"ref_{name}": value for name, value in ev["reference_window"].items()})
        csv_rows.append(row)
    report = exp_dir / "report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    fields = list(dict.fromkeys(name for row in csv_rows for name in row))
    with open(exp_dir / "results.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_rows)
    return report


def play(exp_dir: Path, group, only) -> int:
    sentences = [s for s in selected(only) if group is None or group in s[2]]
    for index, (key, text, _) in enumerate(sentences):
        run_dir = exp_dir / "runs" / key
        if not (run_dir / "train" / "model.pt").exists():
            print(f"[{key}] 학습 결과 없음, 건너뜀: {text}", flush=True)
            continue
        print(f"\n[{index + 1}/{len(sentences)}] {key}: {text}  (창을 닫거나 Ctrl+C → 다음)", flush=True)
        if play_motion.play(run_dir) == 130 and index + 1 < len(sentences):
            if input("다음 문장을 재생할까요? [Enter=다음, q=끝] ").strip().lower() == "q":
                break
    return 0


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("--iters", type=int, default=ITERS, help=f"문장당 학습 반복 (기본 {ITERS})")
    cli.add_argument("--num-envs", type=int, default=tft.DEFAULT_NUM_ENVS, help="병렬 시뮬레이션 수")
    cli.add_argument("--only", help="쉼표로 구분한 문장 키만 (예: base,left)")
    cli.add_argument("--list", action="store_true", help="문장 키와 그룹 출력")
    cli.add_argument("--resume", type=Path, metavar="DIR", help="중단된 실험 폴더에서 이어서 실행")
    cli.add_argument("--summarize", type=Path, metavar="DIR", help="학습 없이 보고서만 다시 생성")
    cli.add_argument("--play", type=Path, metavar="DIR", help="실험 결과를 뷰어로 차례로 재생")
    cli.add_argument("--group", choices=tuple(GROUPS), help="--play와 함께: 이 그룹만 재생")
    args = cli.parse_args()

    if args.list:
        for key, text, groups in SENTENCES:
            print(f"{key:10s} {'/'.join(groups):14s} {text}")
        return 0
    if args.play:
        return play(args.play.resolve(), args.group, args.only)
    if args.summarize:
        print(f"보고서: {summarize(args.summarize.resolve())}")
        return 0

    sentences = selected(args.only)
    exp_dir = args.resume.resolve() if args.resume else HERE / datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    (exp_dir / "runs").mkdir(parents=True, exist_ok=True)
    (exp_dir / "experiment.json").write_text(json.dumps({
        "iters": args.iters, "num_envs": args.num_envs,
        "sentences": [{"key": key, "text": text, "groups": groups} for key, text, groups in sentences],
        "started": datetime.datetime.now().isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=2))
    print(f"실험 폴더: {exp_dir}\n문장 {len(sentences)}개 × {args.iters}회, "
          f"예상 약 {len(sentences) * MINUTES_PER_SENTENCE * args.iters / ITERS:.0f}분", flush=True)

    statuses = {}
    try:
        for index, (key, text, _) in enumerate(sentences):
            print(f"\n===== [{index + 1}/{len(sentences)}] {key}: {text}", flush=True)
            statuses[key] = run_sentence(exp_dir, key, text, args.iters, args.num_envs)
            print(f"===== {key}: {statuses[key]}", flush=True)
    except KeyboardInterrupt:
        print(f"\n중단됨. 이어서 하려면: ./experiments/train_eval/run_experiment.py --resume {rel(exp_dir)}",
              file=sys.stderr)
        summarize(exp_dir)
        return 130

    report = summarize(exp_dir)
    print("\n" + "\n".join(f"{key}: {status}" for key, status in statuses.items()))
    print(f"\n보고서: {report}\n눈 확인: ./experiments/train_eval/run_experiment.py --play {rel(exp_dir)} --group 방향")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
