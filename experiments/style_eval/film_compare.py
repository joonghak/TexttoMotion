#!/home/jong/isaaclab/.venv/bin/python
"""Our trained walk policy next to the 100STYLE style it aims at, moved onto our character, as one video per pair.

Usage on this computer:
    ./experiments/style_eval/film_compare.py experiments/style_eval/sets/compare_existing.json
    ./experiments/style_eval/film_compare.py <pairs.json> --only zombie,old

pairs.json: {"out": "<folder>", "pairs": [{"key": "zombie", "run": "experiments/style_walk/<exp>/<variant>",
"style": "Zombie", "ours": "<label of our policy>", "caption": "<line under the pictures>"}]}; instead of "style" a pair
may list "clips": [{"type": "100style", "style": ...} or {"type": "hml", "file": <HumanML3D joints .npy>, "label": ...}]
(text-to-motion outputs, experiments/t2m_compare/retarget_hml.py), and "seconds" for the video length. With
"blind": true (a blind human study) every character gets the same colour, no names are drawn, and every character is
written as its own video <key>_<method>.mp4/.gif (side above front), method "ours" or the clip's "method".
With "no_text": true nothing is written on the pictures (no names, no view labels, no caption line).
A policy on a chain of actions (experiments/chain, a reference clip that does not loop) is filmed from the start of
its clip, without the warm-up, and holds its last pose once the chain is over, as a generated clip does.
Every pair is filmed in an Isaac Lab run of its own. The policy walks from the start of its reference clip, as in
film.py. The 100STYLE clip (retarget_100style.py: the straightest stretch of its forward walk, the actor's joint
rotations on our character) is played kinematically on a second character, which takes no part in the physics of
the first. Cameras follow each character from the side and from the front. The four pictures are put together
(top: side, bottom: front; left: ours in blue, then the clips in purple, orange, red) from 2 s of walking on;
a generated clip starts with the video and holds its last pose when it ends.
Writes <out>/<key>.mp4 and <key>.gif.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "style_walk"))

import play_motion  # noqa: E402
import train_from_text as tft  # noqa: E402

DEVICE = "cuda:0"
PANEL = (640, 480)
HFOV = 50.0
CAM_DIST = 4.6
PITCH = 6.0              # deg the cameras look down
SMOOTH = 0.15            # share of the way a camera moves to its character per step
WARMUP_S, VIDEO_S = 2.0, 7.8
OURS_COLOR, STYLE_COLOR = 0, 4
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
ENV_GAP = 40.0           # m between the two characters' worlds, diagonally (neither is in the other's pictures)


def film_inside(pair: dict, out_dir: Path) -> int:
    sys.path.insert(0, str(tft.MIMICKIT / "mimickit"))
    import envs.env_builder as env_builder
    import learning.agent_builder as agent_builder
    import envs.text_reward_env as text_reward_env
    import engines.isaac_lab_engine as isaac_lab_engine
    import learning.base_agent as base_agent
    import util.mp_util as mp_util
    import carb
    import math
    import numpy as np
    import torch
    from PIL import Image, ImageDraw, ImageFont
    from play_compare import COLORS, build_camera, recolor, write_video
    from run_style_walk import read_scales
    import retarget_100style as rt
    sys.path.insert(0, str(ROOT / "experiments" / "t2m_compare"))
    import retarget_hml as rh

    run = ROOT / pair["run"]

    def layout(self, n):
        offsets = torch.zeros([n, 2], device=self._device, dtype=torch.float)
        offsets[:, 0] = torch.arange(n, device=self._device) * ENV_GAP
        offsets[:, 1] = torch.arange(n, device=self._device) * ENV_GAP
        return offsets

    isaac_lab_engine.IsaacLabEngine._compute_env_offsets = layout
    env_config, engine_config = env_builder.load_configs(str(run / "config" / "env_play.yaml"),
                                                         str(run / "config" / "engine.yaml"))
    mp_util.init(0, 1, DEVICE, int(np.random.randint(6000, 7000)))
    n_clips = len(clip_specs(pair))
    env = text_reward_env.TextRewardEnv(env_config=env_config, engine_config=engine_config, num_envs=1 + n_clips,
                                        device=DEVICE, visualize=False, record_video=True)
    engine, char_id = env._engine, env._get_char_id()
    blind = bool(pair.get("blind"))  # for a blind human study: one colour, no names, one video per character
    if blind:
        recolor(engine, char_id, [COLORS[OURS_COLOR]] * (1 + n_clips))
    else:
        recolor(engine, char_id, [COLORS[OURS_COLOR]] + [COLORS[c] for c in (STYLE_COLOR, 2, 3, 1, 5)][:n_clips])
    agent = agent_builder.build_agent(str(run / "config" / "agent.yaml"), env, DEVICE)
    agent.load(str(run / "train" / "model.pt"))
    agent.eval()
    agent.set_mode(base_agent.AgentMode.TEST)
    engine.stop_video_recording()
    carb.settings.get_settings().set("/rtx/post/aa/op", 4)
    scale = read_scales(run)
    env._speed_scale[0] = scale["speed"]
    env._cadence_scale[0] = scale["cadence"]
    env._weave_amp[0] = scale.get("weave", 0.0)

    kin = env._kin_char_model
    dt = float(engine.get_timestep())
    seconds = float(pair.get("seconds", VIDEO_S))
    once = "humanoid_chain_" in str(env_config.get("motion_file", ""))  # a chain is filmed once from its start
    warmup, steps = (0 if once else int(round(WARMUP_S / dt))), int(round(seconds / dt))
    no_text = bool(pair.get("no_text"))
    clips, titles, notes = [], [pair["ours"]], []
    for spec in clip_specs(pair):
        if spec["type"] == "100style":
            clip = rt.retarget(spec["style"], (warmup + steps + 2) * dt, kin, device=DEVICE)
            clip["offset"] = 0  # the capture is played through the warm-up, like the policy
            notes.append(f"100STYLE {spec['style']} 구간 시작 {clip['start_frame']} (60 fps), 다리 길이 비 {clip['ratio']:.3f}")
        else:
            clip = rh.retarget(np.load(ROOT / spec["file"]), kin, device=DEVICE, align=blind or bool(spec.get("align")),
                               align_s=seconds)
            clip["offset"] = warmup  # a generated clip starts with the video
            notes.append(f"{spec['file']} 배율 {clip['scale']:.3f}")
        clip["body"] = kin.forward_kinematics(clip["root_pos"], clip["root_rot"], clip["joint_rot"])
        clips.append(clip)
        titles.append(spec.get("label") or f"100STYLE {spec.get('style')} (모션 캡처를 우리 캐릭터로 옮김)")
    n_chars = 1 + len(clips)

    def place_clips(step):
        for c, clip in enumerate(clips, start=1):
            ids = torch.tensor([c], device=DEVICE, dtype=torch.long)
            k = min(max(step - clip["offset"], 0), len(clip["dof"]) - 1)
            engine.set_root_pos(ids, char_id, clip["root_pos"][k:k + 1])
            engine.set_root_rot(ids, char_id, clip["root_rot"][k:k + 1])
            engine.set_root_vel(ids, char_id, 0.0)
            engine.set_root_ang_vel(ids, char_id, 0.0)
            engine.set_dof_pos(ids, char_id, clip["dof"][k:k + 1])
            engine.set_dof_vel(ids, char_id, 0.0)
            engine.set_body_pos(ids, char_id, clip["body"][0][k:k + 1])
            engine.set_body_rot(ids, char_id, clip["body"][1][k:k + 1])
        engine._update_reset_objs()  # written to the simulation now, so that the next render shows it

    cameras = {(c, view): build_camera(engine, f"cmp_{c}_{view}", PANEL, HFOV)
               for c in range(n_chars) for view in ("side", "front")}
    centre = [None] * n_chars

    def aim():
        pos = (engine.get_root_pos(char_id)[:, 0:2] + engine._env_offsets).cpu().numpy()
        pitch = math.radians(PITCH)
        for c in range(n_chars):
            centre[c] = pos[c].copy() if centre[c] is None else centre[c] + SMOOTH * (pos[c] - centre[c])
            target = np.array([centre[c][0], centre[c][1], 0.9])
            look, _ = cameras[(c, "side")]
            look(target + CAM_DIST * np.array([0.0, -math.cos(pitch), math.sin(pitch)]), target)
            look, _ = cameras[(c, "front")]
            look(target + CAM_DIST * np.array([math.cos(pitch), 0.0, math.sin(pitch)]), target)
        engine.get_sim().render()
        return {key: read() for key, (_, read) in cameras.items()}

    font = ImageFont.truetype(FONT, 22)
    small = ImageFont.truetype(FONT, 18)
    bar = 0 if no_text else 44

    def compose(shots):
        if any(shot is None for shot in shots.values()):
            return None
        w, h = PANEL
        image = Image.new("RGB", (n_chars * w, 2 * h + bar), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        for c in range(n_chars):
            for r, view in enumerate(("side", "front")):
                image.paste(Image.fromarray(shots[(c, view)]), (c * w, r * h))
                x, y = c * w + 10, r * h + 8
                if no_text:
                    pass
                elif r == 0:
                    draw.text((x, y), titles[c], font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
                    draw.text((x, y + 30), "옆", font=small, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
                else:
                    draw.text((x, y), "정면", font=small, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            if c:
                draw.line([(c * w, 0), (c * w, 2 * h)], fill=(255, 255, 255), width=3)
        draw.line([(0, h), (n_chars * w, h)], fill=(255, 255, 255), width=3)
        if not no_text:
            draw.text((10, 2 * h + 8), pair.get("caption", ""), font=font, fill=(20, 20, 20))
        return np.asarray(image)

    def compose_one(shots, c):
        """One character alone, side above front, without any name (blind mode)."""
        if any(shot is None for shot in shots.values()):
            return None
        w, h = PANEL
        image = Image.new("RGB", (w, 2 * h), (255, 255, 255))
        for r, view in enumerate(("side", "front")):
            image.paste(Image.fromarray(shots[(c, view)]), (0, r * h))
        ImageDraw.Draw(image).line([(0, h), (w, h)], fill=(255, 255, 255), width=3)
        return np.asarray(image)

    frames, singles = [], [[] for _ in range(n_chars)]
    with torch.no_grad():
        env._rand_reset = False
        obs, info = env.reset()
        place_clips(0)
        for _ in range(30):
            aim()  # renderer warm-up
        centre[:] = [None] * n_chars
        held = False  # the chain is over: the physics stops and every character holds where it is
        for step in range(warmup + steps):
            if not held:
                action = agent._decide_action(obs, info)[0]
                action[1:] = 0.0
                obs, _, done, info = env.step(action)
            place_clips(step + 1)
            shots = aim()
            if step >= warmup:
                if blind:
                    for c in range(n_chars):
                        singles[c].append(compose_one(shots, c))
                else:
                    frames.append(compose(shots))
            if not held and bool(done[0] != 0):
                print(f"{'연속 동작 끝' if once else '주의'}: 우리 정책의 에피소드가 {(step + 1) * dt:.2f}초에 끝남 "
                      f"(flag {int(done[0])})", flush=True)
                if once:
                    held = True
                else:
                    obs, info = env.reset(torch.tensor([0], device=DEVICE, dtype=torch.long))
    out_dir.mkdir(parents=True, exist_ok=True)
    if blind:
        names = ["ours"] + [spec.get("method") or f"clip{c}" for c, spec in enumerate(clip_specs(pair), start=1)]
        for name, shots in zip(names, singles):
            shots = [f for f in shots if f is not None]
            write_video(shots, int(round(1.0 / dt)), out_dir / f"{pair['key']}_{name}.mp4",
                        out_dir / f"{pair['key']}_{name}.gif", gif_width=480)
        print(f"촬영 완료 (blind): {pair['key']} {', '.join(names)}; " + "; ".join(notes) + f" -> {out_dir}", flush=True)
        sys.stdout.flush()
        os._exit(0)
    frames = [f for f in frames if f is not None]
    write_video(frames, int(round(1.0 / dt)), out_dir / f"{pair['key']}.mp4", out_dir / f"{pair['key']}.gif",
                gif_width=min(1920, 480 * n_chars))
    print(f"촬영 완료: {pair['key']} {len(frames)}프레임; " + "; ".join(notes) + f" -> {out_dir}", flush=True)
    sys.stdout.flush()
    os._exit(0)


def clip_specs(pair: dict) -> list:
    """The kinematic characters of a pair: "clips" [{"type": "100style", "style"} or {"type": "hml", "file", "label"}],
    or the older {"style": name} for one 100STYLE clip."""
    if "clips" in pair:
        return pair["clips"]
    return [{"type": "100style", "style": pair["style"]}]


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("pairs", type=Path)
    cli.add_argument("--only", help="쉼표로 구분한 key")
    cli.add_argument("--inside", help=argparse.SUPPRESS)
    args = cli.parse_args()
    spec = json.loads(args.pairs.read_text())
    out_dir = (ROOT / spec["out"]).resolve()
    pairs = spec["pairs"]
    if args.inside:
        return film_inside(next(p for p in pairs if p["key"] == args.inside), out_dir)
    if args.only:
        keep = {k.strip() for k in args.only.split(",")}
        pairs = [p for p in pairs if p["key"] in keep]
    os.environ.setdefault("DISPLAY", play_motion.DEFAULT_DISPLAY)
    os.environ.setdefault("XAUTHORITY", play_motion.DEFAULT_XAUTHORITY)
    out_dir.mkdir(parents=True, exist_ok=True)
    failed = []
    for pair in pairs:
        code = tft.run_in_isaaclab([args.pairs.resolve(), "--inside", pair["key"]],
                                   log_file=out_dir / f"{pair['key']}_console.log", script=Path(__file__).resolve())
        made = out_dir / (f"{pair['key']}_ours.gif" if pair.get("blind") else f"{pair['key']}.gif")
        if code != 0 or not made.exists():
            failed.append(pair["key"])
    print("실패: " + ", ".join(failed) if failed else f"모두 완료 -> {out_dir}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
