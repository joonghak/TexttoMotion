#!/home/jong/isaaclab/.venv/bin/python
"""Numbers behind the style-walk policies: stability, how far each style target is met, posture.

Usage on this computer:
    ./experiments/style_walk/quality_eval.py                                # most recent experiment
    ./experiments/style_walk/quality_eval.py experiments/style_walk/<폴더>
    ./experiments/style_walk/quality_eval.py <폴더> --variants base,strong

All variants of an experiment run in one headless simulation, each character with its
own policy (REPLICAS copies per variant). Results go to <폴더>/quality/:
    curves.png     foot height, hand swing, pelvis height and speed, knee angle, forward reach
                   of a foot (dots = simulated character, dashed = its target) and how
                   often each foot is on the ground, over the gait cycle, from the clip start
    quality.json   per-variant statistics from random-start episodes
    report.md      the same as tables
Targets come from the scales in each variant's env.yaml (1.0 = plain reference) and its formula
(swing_unit, pose_unit).
The report's last table (sideways sway, trunk tilt, pelvis height, knee bend, hand positions)
is measured on the character alone, without any target of the formula.
Pictures of the motion itself: film.py.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

import train_from_text as tft  # noqa: E402
from play_compare import COLORS, latest_experiment  # noqa: E402
from run_style_walk import load_variants, read_formula, read_pose_terms, read_scales, run_clip  # noqa: E402

DEVICE = "cuda:0"
REPLICAS = 128          # characters per variant (384 random-start episodes each)
WARMUP_STEPS = 90       # walk 3 s before logging the curves
CURVE_CYCLES = 4
STAT_STEPS = 900        # 30 s of random-start episodes per character
CONTACT_FORCE = 1.0     # N; a foot counts as on the ground above this
MIN_AIR_STEPS = 4       # steps (0.13 s) a foot has to be off the ground before its touchdown counts as a foot strike
LEAD_GAP = 0.05         # m one foot has to be ahead of the other to count as the leading foot
# joint index groups in joint_err_w order (root excluded)
JOINT_GROUPS = {"torso_head": [0, 1], "arms": [2, 3, 5, 6], "hips_ankles": [8, 10, 11, 13], "knees": [9, 12]}


def launch(exp_dir: Path, variants) -> int:
    missing = [key for key in variants if not (exp_dir / key / "train" / "model.pt").exists()]
    if missing:
        print(f"학습된 모델이 없습니다: {', '.join(missing)} ({exp_dir})", file=sys.stderr)
        return 1
    (exp_dir / "quality").mkdir(exist_ok=True)
    return tft.run_in_isaaclab([exp_dir, "--inside", "--variants", ",".join(variants)],
                               log_file=exp_dir / "quality" / "console.log", script=Path(__file__).resolve())


def evaluate_inside(exp_dir: Path, variants) -> int:
    """Runs under Isaac Lab from the MimicKit directory."""
    sys.path.insert(0, str(tft.MIMICKIT / "mimickit"))
    import envs.env_builder as env_builder
    import learning.agent_builder as agent_builder
    import envs.base_env as base_env
    import envs.text_reward_env as text_reward_env
    import learning.base_agent as base_agent
    import util.mp_util as mp_util
    import util.torch_util as torch_util
    import numpy as np
    import torch

    num_variants = len(variants)
    num_envs = num_variants * REPLICAS
    runs = [exp_dir / key for key in variants]
    config_dir = runs[0] / "config"
    env_config, engine_config = env_builder.load_configs(str(config_dir / "env_play.yaml"), str(config_dir / "engine.yaml"))
    mp_util.init(0, 1, DEVICE, int(np.random.randint(6000, 7000)))
    env = text_reward_env.TextRewardEnv(env_config=env_config, engine_config=engine_config, num_envs=num_envs,
                                        device=DEVICE, visualize=False)
    engine, char_id, kin = env._engine, env._get_char_id(), env._kin_char_model
    agents = []
    for run in runs:
        agent = agent_builder.build_agent(str(run / "config" / "agent.yaml"), env, DEVICE)
        agent.load(str(run / "train" / "model.pt"))
        agent.eval()
        agent.set_mode(base_agent.AgentMode.TEST)
        agents.append(agent)

    # Scales of each variant (1.0 = plain reference), to measure how well its targets are met.
    scales = [read_scales(run) for run in runs]
    variant_of = torch.arange(num_envs, device=DEVICE) % num_variants
    env_ids_of = [(variant_of == v).nonzero(as_tuple=False).flatten() for v in range(num_variants)]
    foot_scale = torch.tensor([s["foot_lift"] for s in scales], device=DEVICE)[variant_of]
    tilt_scale = torch.tensor([s["upright"] for s in scales], device=DEVICE)[variant_of]
    speed_scale = torch.tensor([s["speed"] for s in scales], device=DEVICE)[variant_of]
    # each character follows the reference with its own step length and rhythm
    env._speed_scale[:] = speed_scale
    env._cadence_scale[:] = torch.tensor([s["cadence"] for s in scales], device=DEVICE)[variant_of]
    env._weave_amp[:] = torch.tensor([s.get("weave", 0.0) for s in scales], device=DEVICE)[variant_of]

    def act(obs, info):
        actions = None
        for agent, ids in zip(agents, env_ids_of):
            action = agent._decide_action(obs[ids], info)[0]
            if actions is None:
                actions = torch.zeros([num_envs, action.shape[-1]], device=DEVICE, dtype=action.dtype)
            actions[ids] = action
        return actions

    foot_ids, hand_ids, head_id, arm_ids = env._foot_ids, env._hand_ids, env._head_id, env._arm_joint_ids
    tracked_joints = (env._joint_err_w > 0).nonzero(as_tuple=False).flatten()  # the hands have no joint of their own
    body_names = kin.get_body_names()
    chest_id = body_names.index("torso")
    # each character's own pose changes (arm swing, swing, pose, crouch), so that env._calc_pose_target gives its target pose
    for ids, scale, terms in zip(env_ids_of, scales, [read_pose_terms(run) for run in runs]):
        env._swing_scale[ids] = 1.0
        env._swing_scale[ids.unsqueeze(-1), arm_ids] = scale["arm_swing"]
        env._pose_offset[ids] = torch.tensor([0.0, 0.0, 0.0, 1.0], device=DEVICE)
        for body, value in terms["swing"].items():
            env._swing_scale[ids, body_names.index(body) - 1] = float(value)
        for body, angles in terms["pose"].items():
            exp_map = torch.tensor([angles], device=DEVICE, dtype=torch.float) * (math.pi / 180.0)
            env._pose_offset[ids, body_names.index(body) - 1] = torch_util.exp_map_to_quat(exp_map)
        env._crouch_angle[ids] = math.radians(terms["crouch"])
        env._foot_pitch[ids] = math.radians(terms.get("foot_pitch", 0.0))
    # The env takes its swing unit and arm anchor from the first variant's config; each formula of the
    # variants gets its own, so that every character's target pose is the one it was trained on.
    formula_groups = {}
    for ids, formula in zip(env_ids_of, [read_formula(run) for run in runs]):
        key = (formula["swing_unit"], formula["pose_unit"])
        if key not in formula_groups:
            anchor, lean = env._calc_pose_anchor(key[1]) if key[1] else (None, None)
            formula_groups[key] = {"gain": env._calc_swing_gain(key[0]), "anchor": anchor, "lean": lean, "ids": []}
        formula_groups[key]["ids"].append(ids)
    own_formula = (env._swing_gain, env._pose_anchor, env._pose_lean)

    def pose_target():
        """env._calc_pose_target (thighs x speed scale) with each character's own swing unit and arm anchor."""
        target = None
        for group in formula_groups.values():
            env._swing_gain, env._pose_anchor, env._pose_lean = group["gain"], group["anchor"], group["lean"]
            group_target = env._calc_pose_target(thigh_scale=speed_scale)
            ids = torch.cat(group["ids"])
            if target is None:
                target = group_target
            target[ids] = group_target[ids]
        env._swing_gain, env._pose_anchor, env._pose_lean = own_formula
        return target

    knee_dofs = [kin.get_joint_dof_idx(body_names.index(name)) for name in ("right_shin", "left_shin")]
    elbow_dofs = [kin.get_joint_dof_idx(body_names.index(name)) for name in ("right_lower_arm", "left_lower_arm")]
    elbow_sign = torch.tensor([1.0, -1.0], device=DEVICE)  # the left elbow bends the other way
    ground_h = env._foot_ground_h.unsqueeze(0)
    dt = float(engine.get_timestep())
    length = float(env._motion_lib.get_motion_length(torch.zeros(1, dtype=torch.long, device=DEVICE))[0])
    cycle = int(round(length / dt))
    null_flag, fail_flag = base_env.DoneFlags.NULL.value, base_env.DoneFlags.FAIL.value

    def hand_offset(root_pos, root_rot, body_pos):
        return text_reward_env.calc_forward_offset(root_rot, body_pos[:, hand_ids, :] - root_pos.unsqueeze(-2))

    def foot_reach(root_pos, root_rot, body_pos):
        return text_reward_env.calc_forward_offset(root_rot, body_pos[:, foot_ids, :] - root_pos.unsqueeze(-2))

    def forward_speed(root_rot, root_vel):
        return text_reward_env.calc_forward_offset(root_rot, root_vel.unsqueeze(-2))[:, 0]

    def fallen():
        """A body other than the feet is on the ground: the fall check of the env (the other failure is being 1 m off the target)."""
        forces = engine.get_ground_contact_forces(char_id).clone()
        forces[:, env._contact_body_ids, :] = 0
        return torch.any(torch.abs(forces) > 0.1, dim=-1).any(dim=-1)

    def arm_target(joint_rot, scale):
        """Reference joint rotations [N, J, 4] with the arm motion multiplied by scale [N]."""
        offset_scale = scale.reshape(-1, 1).expand(-1, len(arm_ids)).reshape(-1, 1)
        target = joint_rot.clone()
        target[:, arm_ids, :] = text_reward_env.amplify_about_mean(joint_rot[:, arm_ids, :], env._arm_mean_rot, offset_scale)
        return target

    def measure():
        """Per-character quantities of the current step and their targets."""
        root_pos, root_rot = engine.get_root_pos(char_id), engine.get_root_rot(char_id)
        body_pos = engine.get_body_pos(char_id)
        dof_pos = engine.get_dof_pos(char_id)
        joint_rot = kin.dof_to_rot(dof_pos)
        # The formula's own target pose: arms x arm scale, thighs x speed scale, swing, pose and crouch; the rest as the reference.
        tar_joint_rot = pose_target()
        tar_body_pos, _ = kin.forward_kinematics(env._ref_root_pos, env._ref_root_rot, tar_joint_rot)
        ref_tilt = text_reward_env.calc_tilt(env._ref_body_pos[:, head_id, :] - env._ref_root_pos)
        heading_inv = torch_util.calc_heading_quat_inv(root_rot)
        hand_local = torch_util.quat_rotate(heading_inv.unsqueeze(1).expand(-1, len(hand_ids), -1).reshape(-1, 4),
                                            (body_pos[:, hand_ids, :] - root_pos.unsqueeze(1)).reshape(-1, 3))
        return {
            # the character alone, no target: trunk tilt in its heading frame (roll, pitch, yaw as an exp map),
            # head position, hands from the pelvis (forward, left, up)
            "chest": torch_util.quat_to_exp_map(torch_util.quat_mul(heading_inv, engine.get_body_rot(char_id)[:, chest_id, :])),
            "head_rot": torch_util.quat_to_exp_map(torch_util.quat_mul(heading_inv, engine.get_body_rot(char_id)[:, head_id, :])),
            "elbow": dof_pos[:, elbow_dofs] * elbow_sign,
            "head_pos": body_pos[:, head_id, :],
            "hand_local": hand_local.reshape(-1, len(hand_ids), 3),
            "pos": root_pos, "heading": torch_util.calc_heading(root_rot),
            "foot": body_pos[:, foot_ids, :],
            "foot_target": ground_h + foot_scale.unsqueeze(-1) * (env._ref_body_pos[:, foot_ids, 2] - ground_h),
            "hand": hand_offset(root_pos, root_rot, body_pos),
            "hand_target": hand_offset(env._ref_root_pos, env._ref_root_rot, tar_body_pos),
            "tilt": text_reward_env.calc_tilt(body_pos[:, head_id, :] - root_pos),
            "tilt_target": tilt_scale * ref_tilt,
            "pelvis": root_pos[:, 2], "pelvis_target": env._ref_root_pos[:, 2],
            "speed": forward_speed(env._ref_root_rot, engine.get_root_vel(char_id)),
            "speed_target": forward_speed(env._ref_root_rot, env._ref_root_vel),
            "reach": foot_reach(root_pos, root_rot, body_pos),
            "reach_target": speed_scale.unsqueeze(-1) * foot_reach(env._ref_root_pos, env._ref_root_rot, env._ref_body_pos),
            "knee": dof_pos[:, knee_dofs], "knee_target": kin.rot_to_dof(env._ref_joint_rot)[:, knee_dofs],
            "arm_err": torch_util.quat_diff_angle(joint_rot[:, arm_ids, :], tar_joint_rot[:, arm_ids, :]),
            "pose_err": torch_util.quat_diff_angle(joint_rot, tar_joint_rot)[:, tracked_joints].mean(dim=-1),
            "position_err": torch.linalg.vector_norm((body_pos - root_pos.unsqueeze(1))
                                                     - (tar_body_pos - env._ref_root_pos.unsqueeze(1)), dim=-1).mean(dim=-1),
            "joint_err": torch_util.quat_diff_angle(joint_rot, env._ref_joint_rot),
            "dof_vel": engine.get_dof_vel(char_id),
            "contact": torch.linalg.vector_norm(engine.get_ground_contact_forces(char_id)[:, foot_ids, :], dim=-1) > CONTACT_FORCE,
            "fallen": fallen(),
            "phase": torch.remainder(env._get_motion_times(), length) / length,
        }

    def rollout(steps, rand_reset, warmup=0):
        log = {}
        with torch.no_grad():
            env._rand_reset = rand_reset
            obs, info = env.reset()
            for step in range(warmup + steps):
                obs, _, done, info = env.step(act(obs, info))
                if step >= warmup:
                    values = measure()
                    values["fail"], values["reset"] = done == fail_flag, done != null_flag
                    for name, value in values.items():
                        log.setdefault(name, []).append(value.cpu().clone())
                reset_ids = (done != null_flag).nonzero(as_tuple=False).flatten()
                if len(reset_ids) > 0:
                    obs, info = env.reset(reset_ids)
        return {name: torch.stack(values).numpy() for name, values in log.items()}  # [T, N, ...]

    quality_dir = exp_dir / "quality"

    # Part 1: from the clip start, curves over the gait cycle (first character of each variant).
    curve = rollout(CURVE_CYCLES * cycle, rand_reset=False, warmup=WARMUP_STEPS)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    all_keys = [key for key, _, _ in load_variants(exp_dir)]
    colors = [COLORS[all_keys.index(key) % len(COLORS)] if key in all_keys else plt.cm.tab10(i)
              for i, key in enumerate(variants)]
    panels = [("foot", 0, 2, 1.0, "right foot height (m)"), ("foot", 1, 2, 1.0, "left foot height (m)"),
              ("pelvis", None, None, 1.0, "pelvis height (m)"), ("tilt", None, None, 180 / math.pi, "torso tilt (deg)"),
              ("speed", None, None, 1.0, "pelvis forward speed (m/s)"),
              ("hand", 0, None, 1.0, "right hand, forward of pelvis (m)"), ("hand", 1, None, 1.0, "left hand, forward of pelvis (m)"),
              ("knee", 0, None, 180 / math.pi, "right knee (deg)"), ("knee", 1, None, 180 / math.pi, "left knee (deg)"),
              ("reach", 0, None, 1.0, "right foot, forward of pelvis (m)")]
    fig, axes = plt.subplots(2, 6, figsize=(30, 9))
    panel_axes = list(axes[0, :5]) + list(axes[1, :5])
    bins = np.linspace(0.0, 1.0, cycle + 1)
    for side, ax in enumerate(axes[:, 5]):
        for v, key in enumerate(variants):
            index = np.clip(np.digitize(curve["phase"][:, v], bins) - 1, 0, cycle - 1)
            on_ground = curve["contact"][:, v, side]
            share = [on_ground[index == b].mean() if (index == b).any() else np.nan for b in range(cycle)]
            ax.plot(0.5 * (bins[:-1] + bins[1:]), np.asarray(share) + 0.02 * v, color=colors[v])
        ax.set_title(("right" if side == 0 else "left") + " foot on the ground (share of steps; lines offset)", fontsize=9)
        ax.set_xlabel("gait phase")
    for ax, (name, side, comp, unit, title) in zip(panel_axes, panels):
        for v, key in enumerate(variants):
            sim, target, phase = curve[name][:, v], curve[name + "_target"][:, v], curve["phase"][:, v]
            if side is not None:
                sim, target = sim[:, side], target[:, side]
            if comp is not None:
                sim = sim[:, comp]
            order = np.argsort(phase)
            ax.plot(phase[order], unit * target[order], "--", color=colors[v], lw=1)
            ax.scatter(phase, unit * sim, s=5, color=colors[v], label=key)
        ax.set_title(title + "  (dots = sim, dashed = target)", fontsize=9)
        ax.set_xlabel("gait phase")
    axes[0, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(quality_dir / "curves.png", dpi=80)

    # Targets over one cycle of the reference: clearance per foot, swing range per hand.
    samples = 240
    motion_ids = torch.zeros(samples, dtype=torch.long, device=DEVICE)
    times = torch.arange(samples, device=DEVICE, dtype=torch.float) * (length / samples)
    ref_root_pos, ref_root_rot, _, _, ref_joint_rot, _ = env._motion_lib.calc_motion_frame(motion_ids, times)
    ref_body_pos, _ = kin.forward_kinematics(ref_root_pos, ref_root_rot, ref_joint_rot)
    ref_clearance = (ref_body_pos[:, foot_ids, 2].max(dim=0).values - env._foot_ground_h).cpu().numpy()
    ends = torch.tensor([0.0, length], device=DEVICE)
    end_root_pos = env._motion_lib.calc_motion_frame(motion_ids[:2], ends)[0]
    ref_speed = float(torch.linalg.vector_norm(end_root_pos[1, 0:2] - end_root_pos[0, 0:2])) / length
    travel = (end_root_pos[1, 0:2] - end_root_pos[0, 0:2]).cpu().numpy()
    travel = travel / max(float(np.linalg.norm(travel)), 1e-6)
    side_axis = np.array([-travel[1], travel[0]])  # to the left of the clip's direction of travel
    ref_steps_per_min = 120.0 / length  # two steps per cycle of the clip
    swing_target = []
    for scale in scales:
        target = arm_target(ref_joint_rot, torch.full([samples], scale["arm_swing"], device=DEVICE))
        body_pos, _ = kin.forward_kinematics(ref_root_pos, ref_root_rot, target)
        offset = hand_offset(ref_root_pos, ref_root_rot, body_pos)
        swing_target.append((offset.max(dim=0).values - offset.min(dim=0).values).cpu().numpy())

    # Part 2: random-start episodes, per-step logs for every character.
    data = rollout(STAT_STEPS, rand_reset=True)
    ground = env._foot_ground_h.cpu().numpy()

    def mean_std(values):
        values = np.asarray(values, dtype=np.float64)
        return {"mean": float(values.mean()), "std": float(values.std())} if values.size else {"mean": None, "std": None}

    def side_gap(right, left):
        """Symmetry index (Robinson): difference between the sides as a percentage of their mean; 0 = same."""
        if right is None or left is None or right + left == 0:
            return None
        return float(100.0 * abs(right - left) / (0.5 * (right + left)))

    results = {}
    for v, key in enumerate(variants):
        swing, lift, accel, slide, speed, drift = [[], []], [[], []], [], [], [], []
        head_sway, pelvis_sway, chest_roll, pelvis_travel, knee_swing = [], [], [], [], []

        def sideways_range(points):
            """Range (m) of positions [T, 2] across the clip's direction of travel, their straight-line drift removed."""
            across = points @ side_axis
            steps = np.arange(len(across))
            return float(np.ptp(across - np.polyval(np.polyfit(steps, across, 1), steps)))
        ids = env_ids_of[v].cpu().numpy()
        episodes, lengths, failed_lengths, travelled = 0, [], [], 0.0
        gait_steps = int(round(cycle / scales[v]["cadence"]))  # control steps of one gait cycle of this variant
        target_speed = scales[v]["speed"] * scales[v]["cadence"] * ref_speed
        # Steps: the leading foot (the one further ahead of the pelvis) changes once per step. The time
        # between two changes gives the cadence; it works for running too, where contacts are short.
        step_intervals = []
        for env_id in ids:
            gap = data["reach"][:, env_id, 0] - data["reach"][:, env_id, 1]
            reset = data["reset"][:, env_id]
            lead, last_change = 0, None
            for step in range(STAT_STEPS):
                if step > 0 and reset[step - 1]:
                    lead, last_change = 0, None
                side = 1 if gap[step] > LEAD_GAP else (-1 if gap[step] < -LEAD_GAP else 0)
                if side != 0 and side != lead:
                    if lead != 0:
                        if last_change is not None:
                            step_intervals.append(step - last_change)
                        last_change = step
                    lead = side
        # Foot strikes: a foot touching down after at least MIN_AIR_STEPS in the air (within one episode).
        # All touchdowns, including the foot briefly losing and regaining contact, show how clean the contact is.
        strikes, touchdowns = 0, 0
        for env_id in ids:
            for side in (0, 1):
                on_ground, reset = data["contact"][:, env_id, side], data["reset"][:, env_id]
                air = 0
                for step in range(1, STAT_STEPS):
                    if reset[step - 1]:
                        air = 0
                    elif on_ground[step]:
                        touchdowns += int(not on_ground[step - 1])
                        strikes += int(air >= MIN_AIR_STEPS)
                        air = 0
                    else:
                        air += 1
        steps_per_s = 1.0 / (float(np.mean(step_intervals)) * dt) if step_intervals else 0.0
        for env_id in ids:
            # A reset at step t means step t+1 starts a new episode: cut the log there.
            cuts = [0] + [int(t) + 1 for t in np.nonzero(data["reset"][:, env_id])[0]] + [STAT_STEPS]
            for start, end in zip(cuts[:-1], cuts[1:]):
                if end == start:
                    continue
                episodes += 1
                if data["reset"][end - 1, env_id]:  # ended by the env, not by the end of the log
                    lengths.append((end - start) * dt)
                    if data["fail"][end - 1, env_id]:
                        failed_lengths.append((end - start) * dt)
                travelled += float(np.linalg.norm(data["pos"][end - 1, env_id, 0:2] - data["pos"][start, env_id, 0:2]))
                if end - start < 3:
                    continue
                vel = data["dof_vel"][start:end, env_id]
                accel.append(np.abs(np.diff(vel, axis=0)).mean() / dt)
                foot = data["foot"][start:end, env_id]
                on_ground = data["contact"][start:end, env_id]
                foot_speed = np.linalg.norm(np.diff(foot[:, :, 0:2], axis=0), axis=-1) / dt
                both = on_ground[1:] & on_ground[:-1]
                if both.any():
                    slide.append(foot_speed[both].mean())
                pos, heading = data["pos"][start:end, env_id], np.unwrap(data["heading"][start:end, env_id])
                seconds = (end - start - 1) * dt
                speed.append(np.linalg.norm(pos[-1, 0:2] - pos[0, 0:2]) / seconds)
                drift.append(abs(math.degrees(heading[-1] - heading[0])) / seconds)
                for first in range(start, end - gait_steps + 1, gait_steps):
                    window = slice(first, first + gait_steps)
                    hand = data["hand"][window, env_id]
                    foot_z = data["foot"][window, env_id, :, 2]
                    for side in (0, 1):
                        swing[side].append(hand[:, side].max() - hand[:, side].min())
                        lift[side].append(foot_z[:, side].max() - ground[side])
                    head_sway.append(sideways_range(data["head_pos"][window, env_id, 0:2]))
                    pelvis_sway.append(sideways_range(data["pos"][window, env_id, 0:2]))
                    chest_roll.append(float(np.degrees(np.ptp(data["chest"][window, env_id, 0]))))
                    pelvis_travel.append(float(np.ptp(data["pelvis"][window, env_id])))
                    knee_swing.append(float(np.degrees(np.ptp(data["knee"][window, env_id], axis=0)).mean()))
        contact = data["contact"][:, ids]
        knee, knee_target = np.degrees(data["knee"][:, ids]), np.degrees(data["knee_target"][:, ids])
        joint_err = np.degrees(data["joint_err"][:, ids])
        seconds = STAT_STEPS * dt * len(ids)
        falls = int(data["fail"][:, ids].sum())
        falls_on_ground = int((data["fail"][:, ids] & data["fallen"][:, ids]).sum())
        # Commanded quantities (scale != 1): how far the measured value is from its target.
        swing_mean, lift_mean = [mean_std(x)["mean"] for x in swing], [mean_std(x)["mean"] for x in lift]
        tilt_mean, tilt_target = float(np.degrees(data["tilt"][:, ids]).mean()), float(np.degrees(data["tilt_target"][:, ids]).mean())
        commanded = []
        # Distance covered per second over all episodes: an episode that fails after a few steps counts
        # for those few steps only (in the mean of the episodes' speeds it would count like a full one).
        speed_mean = travelled / (seconds - episodes * dt)
        if scales[v]["speed"] != 1.0 or scales[v]["cadence"] != 1.0:
            commanded.append(("speed", speed_mean, target_speed))
        if scales[v]["cadence"] != 1.0:
            commanded.append(("cadence", 60.0 * steps_per_s, scales[v]["cadence"] * ref_steps_per_min))
        if scales[v]["arm_swing"] != 1.0:
            commanded += [("arm_swing", m, float(t)) for m, t in zip(swing_mean, swing_target[v])]
        if scales[v]["foot_lift"] != 1.0:
            commanded += [("foot_lift", m, float(t)) for m, t in zip(lift_mean, scales[v]["foot_lift"] * ref_clearance)]
        if scales[v]["upright"] != 1.0:
            commanded.append(("upright", tilt_mean, tilt_target))
        command_errors = [100.0 * abs(m - t) / t for _, m, t in commanded if m is not None]
        stance_share = [float(contact[:, :, side].mean()) for side in (0, 1)]
        results[key] = {
            "command_error_pct": float(np.mean(command_errors)) if command_errors else None,
            "command_error_by_term_pct": {name: float(np.mean([100.0 * abs(m - t) / t for n, m, t in commanded if n == name]))
                                          for name in dict.fromkeys(n for n, m, _ in commanded if m is not None)},
            # of the episodes that the env ended (the ones cut by the end of the log are left out)
            "success_pct": 100.0 * (1.0 - falls / max(len(lengths), 1)),
            "episodes_ended": len(lengths),
            "pose_err_deg": float(np.degrees(data["pose_err"][:, ids]).mean()),
            "position_err_cm": float(100.0 * data["position_err"][:, ids].mean()),
            "side_gap_pct": {"foot_clearance": side_gap(*lift_mean), "stance_time": side_gap(*stance_share)},
            "stance_share_right_left": stance_share,
            "falls": falls, "episodes": episodes,
            # failures with a body other than the feet on the ground; the rest ended 1 m away from the target
            "falls_on_ground": falls_on_ground,
            "episode_s": mean_std(lengths),
            "failed_episode_s": mean_std(failed_lengths),
            "failed_episode_max_s": max(failed_lengths) if failed_lengths else None,
            "falls_per_min": float(falls / seconds * 60.0),
            "arm_swing_m": mean_std(swing[0] + swing[1]),
            "arm_swing_right_left_m": [mean_std(swing[0])["mean"], mean_std(swing[1])["mean"]],
            "arm_swing_target_right_left_m": [float(x) for x in swing_target[v]],
            "foot_clearance_m": mean_std(lift[0] + lift[1]),
            "foot_clearance_right_left_m": [mean_std(lift[0])["mean"], mean_std(lift[1])["mean"]],
            "foot_clearance_target_right_left_m": [float(x) for x in scales[v]["foot_lift"] * ref_clearance],
            "torso_tilt_deg": mean_std(np.degrees(data["tilt"][:, ids])),
            "torso_tilt_target_deg": float(np.degrees(data["tilt_target"][:, ids]).mean()),
            "pelvis_height_diff_cm": float(100.0 * (data["pelvis"][:, ids] - data["pelvis_target"][:, ids]).mean()),
            # knee bend while that foot is on the ground: the character's, and the reference's at the same steps
            "stance_knee_deg": float(knee[contact].mean()),
            "stance_knee_reference_deg": float(knee_target[contact].mean()),
            "speed_mps": mean_std(speed),             # per episode
            "speed_overall_mps": speed_mean,          # distance / time over all episodes
            "speed_target_mps": target_speed,
            "steps_per_min": 60.0 * steps_per_s,
            "steps_per_min_target": scales[v]["cadence"] * ref_steps_per_min,
            "foot_strikes_per_min": float(60.0 * strikes / (STAT_STEPS * dt * len(ids))),
            "touchdowns_per_step": float(touchdowns / strikes) if strikes else None,
            "step_length_m": speed_mean / steps_per_s if steps_per_s > 0 else None,
            "heading_drift_dps": mean_std(drift),
            "joint_accel_rad_s2": mean_std(accel),
            "foot_slide_mps": mean_std(slide),
            "joint_err_deg": {name: float(joint_err[:, :, cols].mean()) for name, cols in JOINT_GROUPS.items()},
            "scales": scales[v],
            # the character alone, per gait cycle (sway, roll range) or over all steps (means)
            "head_sway_cm": mean_std(100.0 * np.asarray(head_sway)),
            "pelvis_sway_cm": mean_std(100.0 * np.asarray(pelvis_sway)),
            "chest_roll_range_deg": mean_std(chest_roll),
            "chest_pitch_deg": float(np.degrees(data["chest"][:, ids, 1]).mean()),
            "pelvis_height_m": float(data["pelvis"][:, ids].mean()),
            "pelvis_up_down_cm": mean_std(100.0 * np.asarray(pelvis_travel)),
            "knee_deg": float(knee.mean()),
            "hand_forward_m": float(data["hand_local"][:, ids, :, 0].mean()),
            "hand_apart_m": float((data["hand_local"][:, ids, 1, 1] - data["hand_local"][:, ids, 0, 1]).mean()),
            "hand_up_m": float(data["hand_local"][:, ids, :, 2].mean()),
            "head_pitch_deg": float(np.degrees(data["head_rot"][:, ids, 1]).mean()),
            "elbow_deg": float(np.degrees(data["elbow"][:, ids]).mean()),
            "knee_swing_deg": mean_std(knee_swing),
            # mean absolute error from the variant's own targets
            "arm_target_err_deg": [float(x) for x in np.degrees(data["arm_err"][:, ids]).mean(axis=(0, 1))],
            "foot_target_err_cm": [float(x) for x in 100.0 * np.abs(
                data["foot"][..., 2][:, ids] - data["foot_target"][:, ids]).mean(axis=(0, 1))],
            "tilt_target_err_deg": float(np.degrees(np.abs(data["tilt"][:, ids] - data["tilt_target"][:, ids])).mean()),
        }
    (quality_dir / "quality.json").write_text(json.dumps(
        {"variants": variants, "replicas": REPLICAS, "seconds_per_character": STAT_STEPS * dt,
         "cycle_steps": cycle, "results": results}, ensure_ascii=False, indent=2))

    labels = {key: label for key, label, _ in load_variants(exp_dir)}

    def pm(stat, digits=2):
        return "-" if stat["mean"] is None else f"{stat['mean']:.{digits}f} ± {stat['std']:.{digits}f}"

    def num(value, digits=2, unit=""):
        return "-" if value is None else f"{value:.{digits}f}{unit}"

    def pair(values, digits=2):
        return " / ".join("-" if value is None else f"{value:.{digits}f}" for value in values)

    def percent(values, targets):
        return " / ".join("-" if value is None else f"{100.0 * value / target:.0f}%" for value, target in zip(values, targets))

    lines = ["# 품질 점검 (무작위 시점 시작, 캐릭터당 %.0f초 × %d개)" % (STAT_STEPS * dt, REPLICAS), "",
             "## 핵심 지표", "",
             "| 변형 | 목표 오차율 | 성공률 | 에피소드 길이 (초) | 실패한 에피소드 길이 (초) | 실패 중 넘어짐 | 자세 오차 (°) | 관절 위치 오차 (cm) | 좌우 차이: 발 들기 | 좌우 차이: 디딤 시간 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for key in variants:
        r = results[key]
        error = "-" if r["command_error_pct"] is None else f"{r['command_error_pct']:.1f}%"
        lines.append(f"| {labels.get(key, key)} | {error} | {r['success_pct']:.0f}% ({r['episodes_ended'] - r['falls']}/{r['episodes_ended']}) | "
                     f"{pm(r['episode_s'])} | {pm(r['failed_episode_s'])} (최대 {num(r['failed_episode_max_s'])}) | "
                     f"{r['falls_on_ground']}/{r['falls']} | "
                     f"{r['pose_err_deg']:.1f} | {r['position_err_cm']:.1f} | {num(r['side_gap_pct']['foot_clearance'], 0, '%')} | "
                     f"{num(r['side_gap_pct']['stance_time'], 0, '%')} |")
    lines += ["", "목표 오차율: 바꾸라고 한 값(속도, 걸음 수, 팔 흔들기, 발 들기, 상체 기울기)이 목표에서 벗어난 비율의 평균.",
              "성공률: 10초를 채운 에피소드 ÷ 끝난 에피소드 (실패 = 발 아닌 부위가 땅에 닿거나, 몸 어느 부위든 목표에서 1 m 넘게 벗어남).",
              "에피소드 길이: 실패하거나 10초를 채워 끝난 에피소드의 길이. 실패 중 넘어짐: 발 아닌 부위가 땅에 닿아 끝난 횟수 / 실패 횟수.",
              "자세 오차·관절 위치 오차: 수식이 준 목표 자세(팔·허벅지는 배율 적용)와의 차이,",
              "관절 12개 회전각 평균과 골반 기준 몸 부위 15개 위치 평균. 좌우 차이: |오른−왼| ÷ 평균 (0% = 같음).", "",
             "## 안정성", "",
             "| 변형 | 넘어짐 (횟수/에피소드) | 넘어짐/분 | 속도 (m/s) | 방향 틀어짐 (°/s) | 관절 가속 (rad/s²) | 발 미끄러짐 (m/s) |",
             "|---|---|---|---|---|---|---|"]
    for key in variants:
        r = results[key]
        lines.append(f"| {labels.get(key, key)} | {r['falls']}/{r['episodes_ended']} | {r['falls_per_min']:.2f} | {pm(r['speed_mps'])} | "
                     f"{pm(r['heading_drift_dps'], 1)} | {pm(r['joint_accel_rad_s2'], 1)} | {pm(r['foot_slide_mps'])} |")
    lines += ["", "## 속도와 걸음", "",
              "| 변형 | 속도 (m/s) | 목표 | 달성 | 걸음 수 (걸음/분) | 목표 | 보폭 (m) | 한 걸음당 발 닿는 횟수 |",
              "|---|---|---|---|---|---|---|---|"]
    for key in variants:
        r = results[key]
        speed = r["speed_overall_mps"]
        lines.append(f"| {labels.get(key, key)} | {speed:.2f} | {r['speed_target_mps']:.2f} | "
                     f"{100.0 * speed / r['speed_target_mps']:.0f}% | {r['steps_per_min']:.0f} | {r['steps_per_min_target']:.0f} | "
                     f"{num(r['step_length_m'])} | {num(r['touchdowns_per_step'])} |")
    lines += ["", "속도: 모든 에피소드에서 간 거리 ÷ 시간. 걸음 수: 앞선 발이 바뀌는 간격의 평균으로 계산 (목표는 레퍼런스 한 주기를 두 걸음으로 본 값).",
              "보폭: 속도 ÷ 걸음 수. 한 걸음당 발 닿는 횟수: 발이 땅에 닿은 횟수 ÷ 0.13초 이상 떠 있다가 닿은 횟수.",
              "", "## 목표 달성 (오른쪽 / 왼쪽)", "",
              "| 변형 | 팔 흔들기 (m) | 목표 | 달성 | 발 들기 (m) | 목표 | 달성 | 상체 기울기 (°) | 목표 |",
              "|---|---|---|---|---|---|---|---|---|"]
    for key in variants:
        r = results[key]
        lines.append(f"| {labels.get(key, key)} | {pair(r['arm_swing_right_left_m'])} | {pair(r['arm_swing_target_right_left_m'])} | "
                     f"{percent(r['arm_swing_right_left_m'], r['arm_swing_target_right_left_m'])} | "
                     f"{pair(r['foot_clearance_right_left_m'])} | {pair(r['foot_clearance_target_right_left_m'])} | "
                     f"{percent(r['foot_clearance_right_left_m'], r['foot_clearance_target_right_left_m'])} | "
                     f"{pm(r['torso_tilt_deg'], 1)} | {r['torso_tilt_target_deg']:.1f} |")
    lines += ["", "## 자세", "",
              "| 변형 | 골반 높이 − 레퍼런스 (cm) | 디딤 무릎 굽힘 (°) | 레퍼런스 디딤 무릎 (°) | 레퍼런스 이탈: 몸통·머리 (°) | 팔 | 고관절·발목 | 무릎 |",
              "|---|---|---|---|---|---|---|---|"]
    for key in variants:
        r, err = results[key], results[key]["joint_err_deg"]
        lines.append(f"| {labels.get(key, key)} | {r['pelvis_height_diff_cm']:+.1f} | {r['stance_knee_deg']:.1f} | "
                     f"{r['stance_knee_reference_deg']:.1f} | {err['torso_head']:.1f} | {err['arms']:.1f} | "
                     f"{err['hips_ankles']:.1f} | {err['knees']:.1f} |")
    lines += ["", "## 목표 대비 평균 오차", "",
              "| 변형 | 오른 어깨 (°) | 오른 팔꿈치 | 왼 어깨 | 왼 팔꿈치 | 오른발 높이 (cm) | 왼발 | 상체 기울기 (°) |",
              "|---|---|---|---|---|---|---|---|"]
    for key in variants:
        r = results[key]
        arm, foot = r["arm_target_err_deg"], r["foot_target_err_cm"]
        lines.append(f"| {labels.get(key, key)} | {arm[0]:.1f} | {arm[1]:.1f} | {arm[2]:.1f} | {arm[3]:.1f} | "
                     f"{foot[0]:.1f} | {foot[1]:.1f} | {r['tilt_target_err_deg']:.1f} |")
    lines += ["", "## 자세와 흔들림 (수식의 목표와 무관하게 캐릭터만 잰 값)", "",
              "| 변형 | 머리 좌우 흔들림 (cm) | 골반 좌우 흔들림 (cm) | 상체 좌우 기울기 폭 (°) | 상체 앞 기울기 (°) | 골반 높이 (m) | 골반 위아래 폭 (cm) | 무릎 굽힘 평균 (°) | 손: 골반보다 앞 (m) | 양손 간격 (m) | 손 높이 (m) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for key in variants:
        r = results[key]
        lines.append(f"| {labels.get(key, key)} | {pm(r['head_sway_cm'], 1)} | {pm(r['pelvis_sway_cm'], 1)} | "
                     f"{pm(r['chest_roll_range_deg'], 1)} | {r['chest_pitch_deg']:+.1f} | {r['pelvis_height_m']:.3f} | "
                     f"{pm(r['pelvis_up_down_cm'], 1)} | "
                     f"{r['knee_deg']:.1f} | {r['hand_forward_m']:+.2f} | {r['hand_apart_m']:.2f} | {r['hand_up_m']:+.2f} |")
    lines += ["", "흔들림·기울기·위아래 폭: 걸음 한 주기(레퍼런스 길이 ÷ 걸음 수 배율) 안에서 최대 − 최소의 평균. 좌우 흔들림은 진행 방향에 수직인 위치에서 직선 이동분을 뺀 값.",
              "상체 기울기: 몸통(가슴)이 향한 방향 기준으로 옆(좌우)과 앞으로 기운 각도. 손 위치: 골반 기준, 캐릭터가 향한 방향 좌표."]
    lines += ["", "## 팔·다리·고개 (캐릭터만 잰 값)", "",
              "| 변형 | 팔 흔들기 폭 (m) | 팔꿈치 굽힘 (°) | 무릎 움직임 폭 (°) | 고개 앞 기울기 (°) | 발 들기 (m) | 좌우 차이: 발 들기 | 한 걸음당 발 닿는 횟수 |",
              "|---|---|---|---|---|---|---|---|"]
    for key in variants:
        r = results[key]
        lines.append(f"| {labels.get(key, key)} | {pm(r['arm_swing_m'])} | {r['elbow_deg']:.1f} | {pm(r['knee_swing_deg'], 1)} | "
                     f"{r['head_pitch_deg']:+.1f} | {pm(r['foot_clearance_m'])} | {num(r['side_gap_pct']['foot_clearance'], 0, '%')} | "
                     f"{num(r['touchdowns_per_step'])} |")
    lines += ["", "팔 흔들기 폭: 골반 기준 손의 앞뒤 이동 범위. 무릎 움직임 폭: 걸음 한 주기 안에서 무릎 각도의 최대 − 최소.",
              "고개 앞 기울기: 머리가 향한 방향 기준으로 앞으로 숙인 각도(상체 기울기 포함, 뒤로 젖히면 음수)."]
    (quality_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    print(f"curves: {quality_dir / 'curves.png'}", flush=True)
    return 0


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("exp_dir", nargs="?", help="실험 폴더 (생략하면 가장 최근)")
    cli.add_argument("--variants", help="쉼표로 구분한 변형 폴더 이름 (기본: 폴더의 변형 전부)")
    cli.add_argument("--inside", action="store_true", help=argparse.SUPPRESS)
    args = cli.parse_args()
    exp_dir = Path(args.exp_dir).resolve() if args.exp_dir else latest_experiment()
    if exp_dir is None:
        print(f"실험 결과가 없습니다: {HERE}", file=sys.stderr)
        return 1
    variants = ([key.strip() for key in args.variants.split(",") if key.strip()] if args.variants
                else [key for key, _, _ in load_variants(exp_dir)])
    clips = {run_clip(exp_dir / key) for key in variants}
    if len(clips) > 1:  # one simulation loads one reference clip for every character
        print("참조 모션이 다른 변형은 따로 실행하세요: " + ", ".join(sorted(clips)), file=sys.stderr)
        return 1
    return evaluate_inside(exp_dir, variants) if args.inside else launch(exp_dir, variants)


if __name__ == "__main__":
    raise SystemExit(main())
