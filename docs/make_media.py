"""GIFs and stills of the README, cut from the experiment films (system python3 with OpenCV and Pillow).

    python3 docs/make_media.py

The films themselves (mp4) are not in the repository; they come from experiments/style_walk/film.py and
experiments/style_eval/film_compare.py. Nothing is written on the pictures; the README tables label them.
"""
import os
import shutil
import sys

import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "reports", "final"))
import make_stills as ms  # noqa: E402

OUT = os.path.join(HERE, "media")
STUDY = os.path.join(ROOT, "experiments", "t2m_compare", "study")


def frames(path, start, end, fps_out):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    t, out = start, []
    while t < end and int(round(t * fps)) < n:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
        ok, frame = cap.read()
        if not ok:
            break
        out.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        t += 1.0 / fps_out
    return out


def save_gif(images, path, fps, colors=96):
    median_cut = getattr(getattr(Image, "Quantize", Image), "MEDIANCUT")
    no_dither = getattr(getattr(Image, "Dither", Image), "NONE")
    palette = images[len(images) // 2].quantize(colors=colors, method=median_cut)
    q = [im.quantize(palette=palette, dither=no_dither) for im in images]
    q[0].save(path, save_all=True, append_images=q[1:], duration=int(round(1000 / fps)), loop=0, optimize=True)
    return os.path.getsize(path) / 1e6


def main():
    os.makedirs(OUT, exist_ok=True)
    sizes = {}
    # set 7 styles, each policy filmed alone from 40 degrees off its path (1920 x 720): the middle square
    for key in ["N2", "N4", "N5", "N6", "P5", "P6", "F2", "F4"]:
        ims = frames(os.path.join(ms.SET7, f"fig_{key}_quarter.mp4"), 0.0, 4.0, 12)
        ims = [im.crop((600, 0, 1320, 720)).resize((260, 260), Image.LANCZOS) for im in ims]
        sizes[f"style_{key}"] = save_gif(ims, os.path.join(OUT, f"style_{key}.gif"), 12)
    # the same command by the four methods (human-study films, side view on top of each 640 x 960 film)
    for key, folder in [("set8_Q2", "videos"), ("set9_S2", "videos_report")]:
        for method in ["ours", "momask", "t2mgpt", "mdm"]:
            ims = frames(os.path.join(STUDY, folder, f"{key}_{method}.mp4"), 0.0, 4.0, 12)
            ims = [im.crop((170, 70, 470, 440)).resize((180, 222), Image.LANCZOS) for im in ims]
            sizes[f"{key}_{method}"] = save_gif(ims, os.path.join(OUT, f"compare_{key}_{method}.gif"), 12, colors=64)
    # chains from the side (1920 x 720): a window that follows the character
    for name, colour, end in [("f10_C2", "yellow", 4.1), ("f10_C5", "black", 5.5)]:
        ims = frames(os.path.join(ms.SET10, f"{name}.mp4"), 0.0, end, 12)
        cut = []
        for im in ims:
            x0 = int(min(max(ms.character_x(im, colour) - 200, 0), im.width - 400))
            cut.append(im.crop((x0, 90, x0 + 400, 610)).resize((280, 364), Image.LANCZOS))
        sizes[name] = save_gif(cut, os.path.join(OUT, f"chain_{name}.gif"), 12)
    # stills and the system figure of the report
    for f in ["fig1_architecture.png", "fig2_styles.jpg", "fig3_compare.jpg", "fig4_onesided.jpg", "fig5_chains.jpg"]:
        shutil.copy(os.path.join(ROOT, "reports", "final", "figures", f), os.path.join(OUT, f))
    for k, v in sizes.items():
        print(f"{k:24s} {v:5.2f} MB")
    print("total MB", round(sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1e6, 1))


if __name__ == "__main__":
    main()
