#!/home/jong/isaaclab/.venv/bin/python
"""Did a motion do the requested actions in the requested order? For the chains of set 10 (test_commands_10.json),
on our recorded policies and on text-to-motion outputs alike, from the canonical points of gait_features.

Usage on this computer:
    ./experiments/chain/chain_check.py --trained experiments/style_walk/<experiment>   # our chains (rollouts)
    ./experiments/chain/chain_check.py --hml momask                                    # a T2M model (3 outputs each)

Events over time (all heights above the motion's own floor, the 2nd percentile of the lowest foot point):
- run: the pelvis's ground speed (0.5 s average) above 2.2 m/s for at least 0.4 s (our run 3.6 m/s, walk 1.3 m/s);
- walk: speed between 0.5 and 2.2 m/s for at least 0.8 s;
- jump: both ankles more than 15 cm above the floor at once for at least 0.2 s (a running stride's flight is lower
  and shorter: our run lifts the ankles 6-12 cm in its 0.1-0.15 s flight);
- kick: an ankle more than 60 cm above the floor (our front kick 1.14 m, turning kick 1.62 m, a walking step 15 cm);
- spin: the facing (shoulder line) has turned by more than 180 degrees over the last 1.5 s.
An action's time is the median time of its frames (a few walking-speed frames between two jumps do not make the walk
come first); a chain passes when every requested action occurs and their times are in the requested order (spinkick:
a kick and a spin, at the earlier of the two). Writes the times and the result per motion to <out>/chain_check.md and
.json.
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "style_eval"))
sys.path.insert(0, str(ROOT / "experiments" / "t2m_compare"))

import gait_features as gf  # noqa: E402
import measure as ms  # noqa: E402

SET10 = ROOT / "experiments" / "style_llm" / "test_commands_10.json"
RUN_V, WALK_V = 2.2, (0.5, 2.2)
JUMP_H, JUMP_S, KICK_H = 0.15, 0.2, 0.60


def _kept(mask: np.ndarray, fps: float, min_s: float) -> np.ndarray:
    """mask with its stretches shorter than min_s removed."""
    out, start = np.zeros_like(mask), None
    for t, m in enumerate(np.append(mask, False)):
        if m and start is None:
            start = t
        elif not m and start is not None:
            if (t - start) / fps >= min_s:
                out[start:t] = True
            start = None
    return out


def events(points: np.ndarray, fps: float) -> dict:
    """First start time (s) of each event kind, or None."""
    p = points.astype(np.float64)
    pelvis = p[:, gf.IDX["pelvis"]]
    ankles = np.stack([p[:, gf.IDX["r_ankle"]], p[:, gf.IDX["l_ankle"]]], axis=1)
    toes = np.stack([p[:, gf.IDX["r_toe"]], p[:, gf.IDX["l_toe"]]], axis=1)
    floor = float(np.percentile(np.minimum(ankles[..., 2].min(axis=1), toes[..., 2].min(axis=1)), 2))
    height = ankles[..., 2] - floor
    xy = gf._smooth(pelvis[:, :2], max(1, int(0.5 * fps)))
    speed = np.linalg.norm(np.gradient(xy, 1.0 / fps, axis=0), axis=-1)
    shoulders = p[:, gf.IDX["l_shoulder"], :2] - p[:, gf.IDX["r_shoulder"], :2]
    facing = np.unwrap(np.arctan2(shoulders[:, 1], shoulders[:, 0]))
    window = int(1.5 * fps)
    turn = np.array([np.abs(facing[t] - facing[max(0, t - window):t + 1]).max() for t in range(len(facing))])
    found = {"run": _kept(speed > RUN_V, fps, 0.4), "walk": _kept((speed > WALK_V[0]) & (speed < WALK_V[1]), fps, 0.8),
             "jump": _kept(height.min(axis=1) > JUMP_H, fps, JUMP_S), "kick": _kept(height.max(axis=1) > KICK_H, fps, 0.05),
             "spin": turn > np.pi}
    return {k: (float(np.median(np.nonzero(v)[0])) / fps if v.any() else None) for k, v in found.items()}


def passes(sequence: list, ev: dict) -> bool:
    """Every requested action occurs, at times in the requested order (spinkick: a kick and a spin)."""
    times = []
    for action in sequence:
        if action == "spinkick":
            if ev["kick"] is None or ev["spin"] is None:
                return False
            times.append(min(ev["kick"], ev["spin"]))
        else:
            if ev[action] is None:
                return False
            times.append(ev[action])
    return all(a < b for a, b in zip(times, times[1:]))


def our_points(path: Path):
    """Canonical points of the first episode of each character of a rollout, and the frame rate."""
    data = np.load(path, allow_pickle=True)
    names, fps = list(data["body_names"]), 1.0 / float(data["dt"])
    out = []
    for n in range(data["body_pos"].shape[1]):
        resets = np.nonzero(data["reset"][:, n])[0]
        end = int(resets[0]) if len(resets) and resets[0] > 1 else len(data["reset"])
        out.append(gf.sim_points(data["body_pos"][:end, n].astype(np.float64), data["body_rot"][:end, n].astype(np.float64), names))
    return out, fps


def episodes_cut_short(path: Path, exp: Path, key: str) -> tuple:
    """(episodes that ended more than 0.2 s before the chain's end, all episodes) over the characters: an episode of a
    chain ends with the chain, so a shorter one is a fall (the last, cut by the recording, is not counted)."""
    import pickle

    variant = next(v for v in json.loads((exp / "variants.json").read_text()) if v["key"] == key)
    with open(ROOT / "MimicKit" / "data" / "motions" / "humanoid" / f"humanoid_{variant.get('clip')}.pkl", "rb") as f:
        motion = pickle.load(f)
    # the clip is read cadence times as fast (text_reward_env), so the chain ends that much sooner
    length = (len(motion["frames"]) - 1) / motion["fps"] / float(variant.get("scales", {}).get("cadence", 1.0))
    data = np.load(path, allow_pickle=True)
    dt, short, total = float(data["dt"]), 0, 0
    for n in range(data["reset"].shape[1]):
        ends = np.nonzero(data["reset"][:, n])[0]
        lengths = np.diff(np.concatenate([[0], ends])) * dt
        total += len(lengths)
        short += int(np.sum(lengths < length - 0.2))
    return short, total


def main() -> int:
    commands = [c for c in json.loads(SET10.read_text())["commands"] if c.get("expect_sequence")]
    rows, lines = {}, []
    if sys.argv[1] == "--trained":
        exp = Path(sys.argv[2]).resolve()
        variants = {(v.get("source") or {}).get("id"): v["key"] for v in json.loads((exp / "variants.json").read_text())}
        title, out_dir = f"우리 정책 ({exp.name})", exp
        falls = {}
        for c in commands:
            path = ROOT / "experiments" / "style_eval" / "rollouts" / f"{exp.name}__{variants.get(c['id'])}.npz"
            if c["id"] in variants and path.exists():
                pts, fps = our_points(path)
                rows[c["id"]] = [events(x, fps) for x in pts[:1]]  # the characters replay the same policy
                falls[c["id"]] = episodes_cut_short(path, exp, variants[c["id"]])
    else:
        method = sys.argv[2]
        title, out_dir = method, ROOT / "experiments" / "t2m_compare" / "out"
        for c in commands:
            evs = []
            for f in sorted(glob.glob(str(out_dir / method / f"set10_{c['id']}_r*.npy"))):
                joints = np.load(f)
                evs.append(events(ms.hml_points(joints[0] if joints.ndim == 4 else joints), ms.HML_FPS))
            if evs:
                rows[c["id"]] = evs
    lines = [f"# 연속 동작 순서 확인, {title}", "",
             "동작마다 그 동작으로 판정된 프레임들의 가운데 시각(초)이다. 요청한 동작이 모두 나오고 이 순서이면 통과이다.", "",
             "| ID | 명령 | 요청 순서 | 동작의 시각 (달리기, 걷기, 점프, 차기, 돌기) | 통과 |", "| --- | --- | --- | --- | --- |"]
    total = ok_total = 0
    result = {}
    for c in commands:
        if c["id"] not in rows:
            continue
        oks = [passes(c["expect_sequence"], ev) for ev in rows[c["id"]]]
        total += len(oks)
        ok_total += sum(oks)
        result[c["id"]] = {"events": rows[c["id"]], "pass": oks}
        shown = "; ".join(", ".join(f"{k} {v:.1f}" for k, v in ev.items() if v is not None) or "-" for ev in rows[c["id"]])
        lines.append(f"| {c['id']} | {c['text']} | {' → '.join(c['expect_sequence'])} | {shown} | {sum(oks)}/{len(oks)} |")
    lines += ["", f"통과 {ok_total}/{total}"]
    if sys.argv[1] == "--trained":
        cut = sum(v[0] for v in falls.values())
        lines.append(f"넘어짐: 끝까지 가지 못한 에피소드 {cut}/{sum(v[1] for v in falls.values())} "
                     "(캐릭터 4개 × 30초, 연속 동작이 끝나면 에피소드도 끝난다)")
        for cid, v in falls.items():
            result.setdefault(cid, {})["falls"] = {"short": v[0], "episodes": v[1]}
    name = "chain_check" if sys.argv[1] == "--trained" else f"{sys.argv[2]}_chain_check"
    (out_dir / f"{name}.json").write_text(json.dumps(result, indent=1, default=float))
    (out_dir / f"{name}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
