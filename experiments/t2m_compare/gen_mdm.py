"""MDM (Tevet et al., ICLR 2023) on our commands: the joints the model generates.

Usage on this computer (the baselines' environment):
    /home/jong/baselines/venv/bin/python experiments/t2m_compare/gen_mdm.py prompts.json out_dir [--repeats 3] [--cpu]

The released 50-step model (save/humanml_enc_512_50steps: transformer encoder, CLIP text encoder) with the
classifier-free guidance of its generation (gen_guidance_param 2.5), every prompt at the length given in
prompts.json (frames at 20 fps). The samples are un-normalised with HumanML3D's Mean.npy and Std.npy, as MDM's
text-only dataset does, and turned into joints with recover_from_ric. Only the model and sampling code of the
repository are used: its generate.py also loads a dataset, moviepy and plotting. One seed per repeat. Writes
out_dir/<key>_r<repeat>.npy with joints [T, 22, 3].
"""

from __future__ import annotations

import json
import os
import sys
from argparse import Namespace
from pathlib import Path

MDM = Path("/home/jong/baselines/motion-diffusion-model")
HUMANML = Path("/home/jong/baselines/HumanML3D/HumanML3D")
MODEL = MDM / "save" / "humanml_enc_512_50steps" / "model000750000.pt"


def main() -> int:
    prompts_file, out_dir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    repeats = int(sys.argv[sys.argv.index("--repeats") + 1]) if "--repeats" in sys.argv else 3
    use_cpu = "--cpu" in sys.argv
    prompts = json.loads(prompts_file.read_text())
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(MDM)
    sys.path.insert(0, str(MDM))
    sys.argv = [sys.argv[0]]

    import numpy as np
    import torch
    for alias, value in (("float", float), ("int", int), ("bool", bool), ("object", object)):
        setattr(np, alias, value)
    from data_loaders.humanml.scripts.motion_process import recover_from_ric
    from data_loaders.tensors import collate
    import model.mdm as mdm_module
    from utils.model_util import create_model_and_diffusion
    from utils.sampler_util import ClassifierFreeSampleModel

    class NoSmpl:  # MDM builds an SMPL layer for rotation outputs; the HumanML3D vectors used here never need it
        def __init__(self, *args, **kwargs):
            self.smpl_model = torch.nn.Module()

    mdm_module.Rotation2xyz = NoSmpl

    args = Namespace(**json.loads((MODEL.parent / "args.json").read_text()))
    guidance = float(args.gen_guidance_param)

    class NoData:  # create_model_and_diffusion asks the dataset only whether it has action classes
        dataset = object()

    model, diffusion = create_model_and_diffusion(args, NoData())
    state = torch.load(MODEL, map_location="cpu", weights_only=False)
    missing, unexpected = model.load_state_dict(state.get("model", state), strict=False)
    assert not unexpected and all(k.startswith("clip_model.") for k in missing), (missing[:5], unexpected[:5])
    model = ClassifierFreeSampleModel(model)
    device = torch.device("cuda" if torch.cuda.is_available() and not use_cpu else "cpu")
    model.to(device)
    model.eval()
    mean, std = np.load(HUMANML / "Mean.npy"), np.load(HUMANML / "Std.npy")

    texts = [p["text"] for p in prompts]
    n_frames = max(int(p.get("length", 120)) for p in prompts)
    for r in range(repeats):
        torch.manual_seed(10 + r)
        batch = [{"inp": torch.zeros(n_frames), "tokens": None, "lengths": int(p.get("length", 120)), "text": t}
                 for p, t in zip(prompts, texts)]
        _, kwargs = collate(batch)
        kwargs["y"] = {k: v.to(device) if torch.is_tensor(v) else v for k, v in kwargs["y"].items()}
        kwargs["y"]["scale"] = torch.ones(len(texts), device=device) * guidance
        with torch.no_grad():
            kwargs["y"]["text_embed"] = model.encode_text(texts)
            sample = diffusion.p_sample_loop(model, (len(texts), model.njoints, model.nfeats, n_frames),
                                             clip_denoised=False, model_kwargs=kwargs, skip_timesteps=0,
                                             init_image=None, progress=False, dump_steps=None, noise=None,
                                             const_noise=False)
        motion = sample.cpu().permute(0, 2, 3, 1).numpy() * std + mean          # [B, 1, T, 263]
        joints = recover_from_ric(torch.from_numpy(motion).float(), 22).numpy()  # [B, 1, T, 22, 3]
        for p, j in zip(prompts, joints):
            np.save(out_dir / f"{p['key']}_r{r}.npy", j[0, :int(p.get("length", 120))].astype(np.float32))
        print(f"repeat {r}: {len(prompts)} motions -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
