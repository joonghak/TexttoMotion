#!/home/jong/isaaclab/.venv/bin/python
"""A motion changed only through the reward formula: the reference clip is never modified.

Usage on this computer:
    ./experiments/style_walk/run_style_walk.py                  # set "style": 4 variants x 1000 iterations + measure
    ./experiments/style_walk/run_style_walk.py --set speed --iters 2000
    ./experiments/style_walk/run_style_walk.py --set motions --clip spinkick --iters 2000   # another reference clip
    ./experiments/style_walk/run_style_walk.py --set general --clip run --only sway2,lean --iters 1500
    ./experiments/style_walk/run_style_walk.py --resume experiments/style_walk/<폴더>
    ./experiments/style_walk/run_style_walk.py --summarize experiments/style_walk/<폴더>
    ./experiments/style_walk/play_compare.py                    # all variants side by side in one viewer

Variants share one reference clip (humanoid_walk.pkl unless --clip names another of
MimicKit/data/motions/humanoid/humanoid_<name>.pkl); only the numbers of the reward formula
differ (MimicKit env "text_reward", mimickit/envs/text_reward_env.py). Sets (SETS below):
    style   힘있게 걷기: base, mild (arm x1.3, foot x1.2, tilt x0.8), medium (x1.6, x1.4, x0.6),
            strong (x2.0, x1.7, x0.4)
    speed   걷는 속도: base, slow (x0.75), fast (x1.25) of the reference's ground speed
    speed_range   속도 배율의 범위: x0.2, x0.75, x1, x1.25, x2, x10
    stride_cadence   보폭 배율 s와 걸음 수 배율 n = min(s, 1.5)를 함께: s = 0.75, 1, 1.25, 2
    motions   다른 레퍼런스에서 같은 수식: 그대로, s = 1.25, n = 1.25 (--clip 과 함께)
    general   여러 모션에 쓰는 일반 항: 관절 흔들림 배율(swing), 자세 이동(pose), 다리 굽힘(crouch)과 그 조합
    vars      수식은 하나로 두고 숫자만 바꾼 12가지 걷기: 상체 기울기, 다리 굽힘, 몸통 흔들림, 팔 자세, 조합 둘
    behaviors 같은 수식, 같은 걷기 레퍼런스로 만든 표현들: 살금살금 후보 셋, 힘차게, 껑충껑충, 지쳐서, 당당하게, …
The speed scale s sets the step length (the walking rhythm stays), the cadence scale n the
steps per minute (the clip is read n times as fast); the ground speed is s * n times the
reference's. arm_swing, speed and cadence rescale targets inside the DeepMimic terms, and so do
swing ({body: scale}: a joint's motion about its mean pose), pose ({body: [x, y, z] deg}: a joint's
mean pose turned) and crouch (deg: thighs forward, knees bent twice as far);
foot_lift and upright are added terms. The DeepMimic weights are the same for every variant; base is plain DeepMimic.
Each variant is measured with ../train_eval/rollout_eval.py (one deterministic 10 s
rollout); report.md compares speed, arm swing, foot clearance, and torso tilt.
The folder's variants.json records the variants for film.py, quality_eval.py and play_compare.py.
An entry may name its own reference clip ("clip": "run"); --clip is the default for the others,
and its own formula settings ("formula": {...}), added to the text_reward block of a variant that
has scales (a clip name becomes that clip's file). Without one it gets FORMULA, the formula fixed
on 2026-11-03 (FORMULA.md); "formula": {} trains with the formula before it.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

import train_from_text as tft  # noqa: E402

ROLLOUT_EVAL = ROOT / "experiments" / "train_eval" / "rollout_eval.py"
WALK_CLIP = tft.CLIP_DIR / tft.CLIPS["walk"]
ITERS = 1000
EPISODE_S = 10.0
TRACK_W = 0.6
# The formula fixed on 2026-11-03 (experiments/style_walk/FORMULA.md): style term, swing scales above 1
# in walking units, arm poses measured from the walk's. Variants without a "formula" entry use it;
# "formula": {} gives the formula before (the policies trained up to 2026-11-01).
FORMULA = {"style": {"w": 0.2}, "swing_unit": "walk", "pose_unit": "walk"}
# Added style term -> weight; scale factors come from VARIANTS, sharpness k is set by the env ("auto").
# arm_swing has no weight: it rescales the arm targets inside the DeepMimic terms.
TERMS = {"foot_lift": 0.15, "upright": 0.1}
TERM_NAMES = {"arm_swing": "팔", "foot_lift": "발", "upright": "상체", "speed": "보폭", "cadence": "걸음 수",
              "swing": "흔들림 배율", "pose": "자세 이동", "crouch": "다리 굽힘", "bounce": "위아래 출렁임",
              "foot_pitch": "발끝 세우기", "weave": "갈지자 폭"}
# Scales that change targets inside the DeepMimic terms (no weight of their own).
TARGET_SCALES = ("arm_swing", "speed", "cadence")
# Pose changes inside the DeepMimic terms: per-body dicts (swing, pose) and an angle in degrees (crouch).
POSE_TERMS = ("swing", "pose", "crouch", "bounce", "foot_pitch")
ARMS_FORWARD = {"right_upper_arm": [0, -85, 0], "left_upper_arm": [0, -85, 0],
                "right_lower_arm": [0, 0, -30], "left_lower_arm": [0, 0, 30]}  # elbows straightened
ARMS_OUT = {"right_upper_arm": [-80, 0, 0], "left_upper_arm": [80, 0, 0]}


def arms_sideways(angle: float) -> dict:
    """Both arms lifted sideways by angle (deg) from where the clip holds them."""
    return {"right_upper_arm": [-angle, 0, 0], "left_upper_arm": [angle, 0, 0]}


def arms_forward(angle: float) -> dict:
    """Both arms lifted forward by angle (deg)."""
    return {"right_upper_arm": [0, -angle, 0], "left_upper_arm": [0, -angle, 0]}


def elbows_bent(angle: float) -> dict:
    """Both elbows bent further by angle (deg); negative straightens them."""
    return {"right_lower_arm": [0, 0, angle], "left_lower_arm": [0, 0, -angle]}


def both(right: str, left: str, value) -> dict:
    """The same swing scale for a left/right pair of bodies."""
    return {right: value, left: value}


KNEES, ELBOWS = ("right_shin", "left_shin"), ("right_lower_arm", "left_lower_arm")
# set -> [(key, label, {term: scale})]; an empty dict is plain DeepMimic. Terms left out stay at 1.
SETS = {
    "style": [
        ("base", "기본 걷기", {}),
        ("mild", "약간 힘있게", {"arm_swing": 1.3, "foot_lift": 1.2, "upright": 0.8}),
        ("medium", "힘있게", {"arm_swing": 1.6, "foot_lift": 1.4, "upright": 0.6}),
        ("strong", "아주 힘있게", {"arm_swing": 2.0, "foot_lift": 1.7, "upright": 0.4}),
    ],
    "speed": [
        ("base", "기본 걷기", {}),
        ("slow", "천천히", {"speed": 0.75}),
        ("fast", "빠르게", {"speed": 1.25}),
    ],
    "speed_range": [
        ("s0_2", "s = 0.2", {"speed": 0.2}),
        ("s0_75", "s = 0.75", {"speed": 0.75}),
        ("s1", "s = 1", {}),
        ("s1_25", "s = 1.25", {"speed": 1.25}),
        ("s2", "s = 2", {"speed": 2.0}),
        ("s10", "s = 10", {"speed": 10.0}),
    ],
    # Cadence n = min(s, 1.5). People keep step length / cadence (the walk ratio) about constant
    # over walking speeds (Sekiya & Nagasaki 1998), so n = s; above about 175 steps per minute
    # (n = 1.5) it would leave the range of human gaits, running included.
    "stride_cadence": [
        ("s0_75_n0_75", "s = 0.75, n = 0.75", {"speed": 0.75, "cadence": 0.75}),
        ("s1", "s = 1, n = 1", {}),
        ("s1_25_n1_25", "s = 1.25, n = 1.25", {"speed": 1.25, "cadence": 1.25}),
        ("s2_n1_5", "s = 2, n = 1.5", {"speed": 2.0, "cadence": 1.5}),
    ],
    "motions": [
        ("base", "s = 1, n = 1", {}),
        ("s1_25", "s = 1.25", {"speed": 1.25}),
        ("n1_25", "n = 1.25", {"cadence": 1.25}),
    ],
    # Train a subset with --only; the torso's swing in the run clip is four times the walk's, hence sway2.
    "general": [
        ("base", "그대로", {}),
        ("sway", "몸통 흔들림 x5", {"swing": {"torso": 5.0}}),
        ("sway2", "몸통 흔들림 x2", {"swing": {"torso": 2.0}}),
        ("lean", "상체 숙임 20°", {"pose": {"torso": [0, 20, 0]}}),
        ("crouch", "다리 굽힘 20°", {"crouch": 20.0}),
        ("arms_out", "팔 벌림 80°", {"pose": ARMS_OUT}),
        # 좀비 클립에서 잰 값: 걸음 수 0.61배, 보폭 0.86배, 팔 흔들기 0.3배, 상체 11° 숙임, 몸통 흔들림 5.8배
        ("zombie", "좀비 조합", {"pose": {**ARMS_FORWARD, "torso": [0, 10, 0]}, "swing": {"torso": 5.0},
                             "arm_swing": 0.3, "speed": 0.85, "cadence": 0.6}),
    ],
    # One formula, twelve sets of numbers. Every target stays within 0.75 m of the reference pose
    # (the episode ends at 1 m): arms lifted beyond about 100 degrees would not.
    "vars": [
        ("base", "기본", {}),
        ("lean_m15", "상체 뒤로 15°", {"pose": {"torso": [0, -15, 0]}}),
        ("lean20", "상체 앞으로 20°", {"pose": {"torso": [0, 20, 0]}}),
        ("lean40", "상체 앞으로 40°", {"pose": {"torso": [0, 40, 0]}}),
        ("crouch15", "다리 굽힘 15°", {"crouch": 15.0}),
        ("crouch30", "다리 굽힘 30°", {"crouch": 30.0}),
        ("sway5", "몸통 흔들림 5배", {"swing": {"torso": 5.0}}),
        ("sway10", "몸통 흔들림 10배", {"swing": {"torso": 10.0}}),
        ("sway10_slow", "몸통 흔들림 10배, 걸음 수 0.6배", {"swing": {"torso": 10.0}, "cadence": 0.6}),
        ("arms45", "팔 옆으로 45°", {"pose": arms_sideways(45)}),
        ("arms90", "팔 옆으로 90°", {"pose": arms_sideways(90)}),
        ("zombie", "좀비 조합", {"pose": {**ARMS_FORWARD, "torso": [0, 10, 0]}, "swing": {"torso": 5.0},
                             "arm_swing": 0.3, "speed": 0.85, "cadence": 0.6}),
        ("sneak", "살금살금 조합", {"crouch": 30.0, "pose": {"torso": [0, 20, 0]}, "arm_swing": 0.3,
                              "speed": 0.6, "cadence": 0.7}),
    ],
    # Expressions made from the walk clip with the same formula. Bending the legs (crouch) also bends
    # the swinging knee, which lifts the foot high; a knee swing below 1 brings the lift back to normal.
    "behaviors": [
        ("base", "기본 걷기", {}),
        ("sneak_a", "살금살금 A", {"crouch": 20.0, "swing": both(*KNEES, 0.7), "speed": 0.8, "cadence": 0.6,
                                 "arm_swing": 0.3, "pose": {"torso": [0, 20, 0], **arms_forward(20), **elbows_bent(40)}}),
        ("sneak_b", "살금살금 B", {"crouch": 25.0, "swing": both(*KNEES, 0.6), "speed": 0.7, "cadence": 0.6,
                                 "arm_swing": 0.2, "pose": {"torso": [0, 25, 0], "head": [0, -15, 0],
                                                            **arms_forward(30), **elbows_bent(50)}}),
        ("sneak_c", "살금살금 C", {"crouch": 15.0, "swing": both(*KNEES, 0.8), "speed": 1.0, "cadence": 0.5,
                                 "arm_swing": 0.3, "pose": {"torso": [0, 15, 0], **arms_forward(20), **elbows_bent(40)}}),
        ("power", "힘차게", {"arm_swing": 1.8, "speed": 1.2, "cadence": 1.15,
                          "pose": {"torso": [0, -5, 0], **elbows_bent(45)}}),
        ("bouncy", "껑충껑충", {"crouch": 15.0, "swing": both(*KNEES, 1.5), "cadence": 1.2, "arm_swing": 1.5}),
        ("tired", "지쳐서 터벅터벅", {"swing": both(*KNEES, 0.8), "speed": 0.8, "cadence": 0.75, "arm_swing": 0.4,
                                  "pose": {"torso": [0, 15, 0], "head": [0, 25, 0]}}),
        ("proud", "당당하게", {"speed": 1.15, "arm_swing": 1.4, "pose": {"torso": [0, -12, 0], "head": [0, -10, 0]}}),
        ("mincing", "종종걸음", {"speed": 0.5, "cadence": 1.5, "arm_swing": 0.6}),
        ("striding", "성큼성큼", {"speed": 1.5, "cadence": 0.85, "arm_swing": 1.3}),
        ("robot", "로봇처럼", {"swing": {"torso": 0.0, **both(*ELBOWS, 0.0), **both(*KNEES, 0.7)}, "pose": elbows_bent(50)}),
        ("old", "노인처럼", {"crouch": 10.0, "swing": both(*KNEES, 0.8), "speed": 0.6, "cadence": 0.8, "arm_swing": 0.4,
                          "pose": {"torso": [0, 30, 0], "head": [0, -10, 0]}}),
        # one variable at a time, for what each number does on its own
        ("arm03", "팔 흔들기 0.3배", {"arm_swing": 0.3}),
        ("arm18", "팔 흔들기 1.8배", {"arm_swing": 1.8}),
        ("knee07", "무릎 흔들림 0.7배", {"swing": both(*KNEES, 0.7)}),
        ("head30", "고개 숙임 30°", {"pose": {"head": [0, 30, 0]}}),
        ("elbow60", "팔꿈치 60° 굽힘", {"pose": elbows_bent(60)}),
        # milder versions of the three behaviors whose feet came out uneven (foot lift differing left and right)
        ("mincing2", "종종걸음 (완화)", {"speed": 0.6, "cadence": 1.35, "arm_swing": 0.6}),
        ("robot2", "로봇처럼 (완화)", {"swing": {"torso": 0.0, **both(*ELBOWS, 0.0), **both(*KNEES, 0.85)}, "pose": elbows_bent(50)}),
        ("power2", "힘차게 (완화)", {"arm_swing": 1.6, "speed": 1.15, "cadence": 1.1,
                                "pose": {"torso": [0, -5, 0], **elbows_bent(45)}}),
    ],
}
VARIANTS = SETS["style"]  # experiment folders without a variants.json


def run_clip(run_dir: Path) -> str:
    """Reference clip file of a run ("humanoid_run.pkl"), from the motion_file of its env.yaml."""
    for line in (Path(run_dir) / "config" / "env.yaml").read_text().splitlines():
        if line.startswith("motion_file:"):
            return Path(line.split(":", 1)[1].strip()).name
    return ""


def variant_clips(exp_dir: Path) -> dict:
    """{key: clip name} of the variants.json entries that name their own reference clip."""
    variants_file = Path(exp_dir) / "variants.json"
    if not variants_file.exists():
        return {}
    return {v["key"]: v["clip"] for v in json.loads(variants_file.read_text()) if v.get("clip")}


def variant_formulas(exp_dir: Path) -> dict:
    """{key: formula settings} of the variants.json entries (added to their text_reward block), FORMULA if not given."""
    variants_file = Path(exp_dir) / "variants.json"
    if not variants_file.exists():
        return {}
    return {v["key"]: v.get("formula", FORMULA) for v in json.loads(variants_file.read_text())}


def load_variants(exp_dir: Path) -> list:
    """[(key, label, scales)] of an experiment folder, in display order."""
    variants_file = Path(exp_dir) / "variants.json"
    if variants_file.exists():
        return [(v["key"], v["label"], v["scales"]) for v in json.loads(variants_file.read_text())]
    return VARIANTS


def read_scales(run_dir: Path) -> dict:
    """Scale of every term of a trained run, from its env.yaml (1.0 = plain reference)."""
    import yaml

    terms = yaml.safe_load((Path(run_dir) / "config" / "env.yaml").read_text()).get("text_reward") or {}
    scales = {name: float((terms.get(name) or {}).get("scale", 1.0)) for name in TARGET_SCALES + tuple(TERMS)}
    scales["weave"] = float((terms.get("weave") or {}).get("amplitude", 0.0))  # m, 0 = a straight path
    return scales


def read_pose_terms(run_dir: Path) -> dict:
    """swing {body: scale}, pose {body: [x, y, z] deg} and crouch (deg) of a trained run, from its env.yaml."""
    import yaml

    terms = yaml.safe_load((Path(run_dir) / "config" / "env.yaml").read_text()).get("text_reward") or {}
    return {"swing": dict(terms.get("swing") or {}), "pose": dict(terms.get("pose") or {}),
            "crouch": float((terms.get("crouch") or {}).get("angle", 0.0)),
            "bounce": float((terms.get("bounce") or {}).get("angle", 0.0)),
            "foot_pitch": float((terms.get("foot_pitch") or {}).get("angle", 0.0))}


def read_formula(run_dir: Path) -> dict:
    """swing_unit and pose_unit clip files of a trained run (None if it does not use one), from its env.yaml."""
    import yaml

    terms = yaml.safe_load((Path(run_dir) / "config" / "env.yaml").read_text()).get("text_reward") or {}
    return {"swing_unit": terms.get("swing_unit"), "pose_unit": terms.get("pose_unit")}


def describe_scales(scales: dict) -> str:
    """One line for the report: 팔 1.3, 흔들림 배율 torso 5, 자세 이동 torso [0, 20, 0]."""
    parts = []
    for name, value in scales.items():
        if isinstance(value, dict):
            value = ", ".join(f"{body} {v:g}" if not isinstance(v, list) else f"{body} {v}" for body, v in value.items())
            parts.append(f"{TERM_NAMES[name]} ({value})")
        else:
            parts.append(f"{TERM_NAMES[name]} {value:g}")
    return ", ".join(parts)


def clip_file(name: str) -> Path:
    """Reference clip humanoid_<name>.pkl of MimicKit."""
    file = tft.CLIP_DIR / f"humanoid_{name}.pkl"
    if not file.exists():
        raise SystemExit(f"레퍼런스가 없습니다: {file}")
    return file


def write_run_files(run_dir: Path, key: str, label: str, scales: dict, clip: Path = WALK_CLIP,
                    formula: dict | None = None) -> dict:
    """Configs and a summary.json in the layout of train_from_text.py runs."""
    import shutil

    import yaml

    config_dir = run_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    env = yaml.safe_load(tft.BASE_ENV_CONFIG.read_text())
    env.update(env_name="text_reward", motion_file=str(clip), episode_length=EPISODE_S)
    if scales:
        env["text_reward"] = {"track_w": TRACK_W}
        for name, scale in scales.items():
            if name in TARGET_SCALES:
                env["text_reward"][name] = {"scale": scale}
            elif name == "weave":
                env["text_reward"][name] = {"amplitude": scale}
            elif name in POSE_TERMS:
                env["text_reward"][name] = {"angle": scale} if name in ("crouch", "bounce", "foot_pitch") else scale
            else:
                env["text_reward"][name] = {"w": TERMS[name], "scale": scale, "k": "auto"}
        for name, value in (formula or {}).items():
            env["text_reward"][name] = str(clip_file(value)) if name in ("swing_unit", "pose_unit") else value
    (config_dir / "env.yaml").write_text(yaml.safe_dump(env, sort_keys=False, allow_unicode=True))
    play = {**env, "rand_reset": False, "visualize_ref_char": False}
    (config_dir / "env_play.yaml").write_text(yaml.safe_dump(play, sort_keys=False, allow_unicode=True))
    shutil.copy(tft.BASE_AGENT_CONFIG, config_dir / "agent.yaml")
    shutil.copy(tft.ENGINE_CONFIG, config_dir / "engine.yaml")
    return {
        "command": label,
        "variant": {"key": key, "label": label, "scales": scales, "terms": env.get("text_reward")},
        "reference": {"clip": str(clip), "duration_s": EPISODE_S},
    }


def is_trained(run_dir: Path) -> bool:
    summary_file = run_dir / "summary.json"
    return (summary_file.exists() and (run_dir / "train" / "model.pt").exists()
            and json.loads(summary_file.read_text())["training"]["status"] == "completed")


def being_trained(run_dir: Path) -> bool:
    """Another process is training this run right now: its summary says so and its console log is still growing."""
    summary_file, log_file = run_dir / "summary.json", run_dir / "train_console.log"
    if not (summary_file.exists() and log_file.exists()):
        return False
    running = json.loads(summary_file.read_text()).get("training", {}).get("status") == "running"
    return running and time.time() - log_file.stat().st_mtime < 300.0


def run_variant(exp_dir: Path, key: str, label: str, scales: dict, iters: int, num_envs: int,
                clip: Path = WALK_CLIP, formula: dict | None = None) -> str:
    import yaml

    run_dir = exp_dir / key
    while being_trained(run_dir):  # two runners may share a folder: the second one waits for the first one's run
        time.sleep(30)
    if not is_trained(run_dir):
        summary = write_run_files(run_dir, key, label, scales, clip, formula)
        steps = yaml.safe_load((run_dir / "config" / "agent.yaml").read_text())["steps_per_iter"]
        config = run_dir / "config"
        args = ["--mode", "train", "--num_envs", num_envs, "--devices", "cuda:0",
                "--engine_config", config / "engine.yaml", "--env_config", config / "env.yaml",
                "--agent_config", config / "agent.yaml", "--visualize", "false", "--video", "false",
                "--rand_seed", tft.RAND_SEED, "--logger", "txt", "--max_samples", iters * num_envs * steps,
                "--out_dir", run_dir / "train"]
        summary["training"] = {"iterations": iters, "num_envs": num_envs, "status": "running",
                               "started": datetime.datetime.now().isoformat(timespec="seconds")}
        (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
        try:
            code = tft.run_in_isaaclab(args, log_file=run_dir / "train_console.log")
        except KeyboardInterrupt:
            code = 130
        summary["training"].update({
            "status": "completed" if code == 0 else ("interrupted" if code == 130 else f"failed (exit {code})"),
            "finished": datetime.datetime.now().isoformat(timespec="seconds"),
            "final_log": tft.read_final_log_row(run_dir / "train" / "log.txt"),
        })
        (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
        if code == 130:
            raise KeyboardInterrupt
        if code != 0:
            return f"학습 실패 (exit {code})"
    if not (run_dir / "eval.json").exists():
        code = tft.run_in_isaaclab([run_dir], log_file=run_dir / "eval_console.log", script=ROLLOUT_EVAL)
        if code != 0:
            return f"측정 실패 (exit {code})"
    return "완료"


def fmt(value, unit="", digits=2):
    return "-" if value is None else f"{value:.{digits}f}{unit}"


def summarize(exp_dir: Path) -> Path:
    variants = load_variants(exp_dir)
    first = exp_dir / variants[0][0] / "summary.json"
    clip = Path(json.loads(first.read_text())["reference"]["clip"]).name if first.exists() else WALK_CLIP.name
    clips = variant_clips(exp_dir)  # only when the variants imitate different clips
    reference = (f"- 레퍼런스: 변형마다 다름 (변형 이름 뒤 괄호), 보상 수식의 배율만 다름" if clips
                 else f"- 레퍼런스: {clip} 원본 (모두 같음), 보상 수식의 배율만 다름")
    lines = ["# 보상 수식의 숫자만 바꾼 비교 (레퍼런스 고정)", "",
             f"- 폴더: {exp_dir}", reference,
             f"- 재생: `./experiments/style_walk/play_compare.py {os.path.relpath(exp_dir, ROOT)}`", "",
             "| 변형 | 배율 | 속도 | 팔 흔들기 폭 | 발 들기 높이 | 상체 기울기 | 완주 | 스텝당 보상 | 학습 |",
             "|---|---|---|---|---|---|---|---|---|"]
    reference_row = None
    for key, label, scales in variants:
        run_dir = exp_dir / key
        summary = json.loads((run_dir / "summary.json").read_text()) if (run_dir / "summary.json").exists() else {}
        ev = json.loads((run_dir / "eval.json").read_text()) if (run_dir / "eval.json").exists() else None
        training = summary.get("training", {})
        final = training.get("final_log") or {}
        per_step = final["Test_Return"] / final["Test_Episode_Length"] if final.get("Test_Episode_Length") else None
        minutes = None
        if training.get("finished"):
            minutes = (datetime.datetime.fromisoformat(training["finished"])
                       - datetime.datetime.fromisoformat(training["started"])).total_seconds() / 60.0
        sim = ev["sim"] if ev else {}
        if ev and not scales:
            reference_row = ev["reference_window"]
        coeff = "추적만" if not scales else describe_scales(scales)
        iters = training.get("iterations")
        if clips:
            label = f"{label} ({clips.get(key, 'walk')})"
        lines.append(f"| {label} | {coeff} | {fmt(sim.get('speed_mps'), ' m/s')} | {fmt(sim.get('arm_swing_m'), ' m')} | "
                     f"{fmt(sim.get('foot_clearance_m'), ' m')} | {fmt(sim.get('torso_tilt_deg'), '°', 1)} | "
                     f"{fmt(ev and ev['completion'] * 100, '%', 0)} | {fmt(per_step)} | "
                     f"{'-' if iters is None else f'{iters}회'} {fmt(minutes, '분', 0)} |")
    if reference_row and not clips:  # with several clips there is no one reference to show
        lines.append(f"| (레퍼런스 원본) | - | {fmt(reference_row.get('speed_mps'), ' m/s')} | "
                     f"{fmt(reference_row.get('arm_swing_m'), ' m')} | {fmt(reference_row.get('foot_clearance_m'), ' m')} | "
                     f"{fmt(reference_row.get('torso_tilt_deg'), '°', 1)} | - | - | - |")
    lines += ["", "속도: 10초 동안 간 거리 ÷ 시간. 팔 흔들기 폭: 골반 기준 손의 앞뒤 이동 범위(양손 평균).",
              "발 들기 높이: 발이 가장 낮을 때 대비 최고 높이. 상체 기울기: 골반→머리 선이 수직에서 기운 평균 각도.",
              "모두 10초 재생 한 번(처음부터, 결정적 정책)으로 측정."]
    report = exp_dir / "report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("--set", choices=tuple(SETS), default="style", help="변형 묶음 (기본 style)")
    cli.add_argument("--clip", default="walk", help="레퍼런스 이름: humanoid_<이름>.pkl (기본 walk)")
    cli.add_argument("--iters", type=int, default=ITERS, help=f"변형당 학습 반복 (기본 {ITERS})")
    cli.add_argument("--num-envs", type=int, default=tft.DEFAULT_NUM_ENVS, help="병렬 시뮬레이션 수")
    cli.add_argument("--out", type=Path, help="실험 폴더 (기본 experiments/style_walk/<시각>)")
    cli.add_argument("--only", help="쉼표로 구분한 변형만 그 순서대로 실행 (예: base,medium)")
    cli.add_argument("--deadline", metavar="HH:MM", help="이 시각(다음 도래)까지 끝낼 수 없는 학습은 시작하지 않음")
    cli.add_argument("--est-min", type=float, default=32.0,
                     help="--deadline 판단에 쓰는 변형당 시간(분, 기본 32). 이번 실행에서 잰 시간이 더 길면 그 값")
    cli.add_argument("--resume", type=Path, metavar="DIR", help="중단된 실험 폴더에서 이어서 실행")
    cli.add_argument("--summarize", type=Path, metavar="DIR", help="학습 없이 보고서만 다시 생성")
    args = cli.parse_args()

    if args.summarize:
        print(f"보고서: {summarize(args.summarize.resolve())}")
        return 0
    exp_dir = (args.resume or args.out or HERE / datetime.datetime.now().strftime("%Y%m%d_%H%M%S")).resolve()
    exp_dir.mkdir(parents=True, exist_ok=True)
    if not (args.resume and ((exp_dir / "variants.json").exists() or (exp_dir / "base").exists())):
        (exp_dir / "variants.json").write_text(json.dumps(
            [{"key": key, "label": label, "scales": scales} for key, label, scales in SETS[args.set]],
            ensure_ascii=False, indent=2))
    only = [key.strip() for key in args.only.split(",")] if args.only else None
    variants = load_variants(exp_dir)
    clips = variant_clips(exp_dir)
    formulas = variant_formulas(exp_dir)
    if only is not None:
        by_key = {variant[0]: variant for variant in variants}
        variants = [by_key[key] for key in only if key in by_key]
    deadline = None
    if args.deadline:
        hour, minute = (int(part) for part in args.deadline.split(":"))
        now = datetime.datetime.now()
        deadline = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if deadline <= now:
            deadline += datetime.timedelta(days=1)
    print(f"실험 폴더: {exp_dir}\n변형 {len(variants)}개 × {args.iters}회"
          + (f", 마감 {deadline:%m-%d %H:%M}" if deadline else ""), flush=True)
    statuses = {}
    longest = args.est_min * 60.0  # seconds one variant may take, raised to the longest one measured here
    try:
        for index, (key, label, scales) in enumerate(variants):
            needs_training = not is_trained(exp_dir / key)
            if deadline and needs_training and \
                    datetime.datetime.now() + datetime.timedelta(seconds=longest) > deadline:
                print(f"\n마감 {deadline:%H:%M} 전에 끝낼 수 없어 {key}부터는 시작하지 않음", flush=True)
                statuses.update({k: "마감으로 건너뜀" for k, _, _ in variants[index:]})
                break
            print(f"\n===== [{index + 1}/{len(variants)}] {key}: {label}", flush=True)
            started = time.time()
            clip = clip_file(clips.get(key, args.clip))
            statuses[key] = run_variant(exp_dir, key, label, scales, args.iters, args.num_envs, clip,
                                        formulas.get(key, FORMULA))
            if needs_training:
                longest = max(longest, time.time() - started)
            print(f"===== {key}: {statuses[key]}", flush=True)
    except KeyboardInterrupt:
        print(f"\n중단됨. 이어서: ./experiments/style_walk/run_style_walk.py --resume {os.path.relpath(exp_dir, ROOT)}",
              file=sys.stderr)
        summarize(exp_dir)
        return 130
    report = summarize(exp_dir)
    print("\n" + "\n".join(f"{key}: {status}" for key, status in statuses.items()))
    print(f"\n보고서: {report}\n재생: ./experiments/style_walk/play_compare.py {os.path.relpath(exp_dir, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
