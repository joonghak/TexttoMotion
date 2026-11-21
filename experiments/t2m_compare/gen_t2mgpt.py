"""T2M-GPT (Zhang et al., CVPR 2023) on our commands: the joints the model generates.

Usage on this computer (the baselines' environment):
    /home/jong/baselines/venv/bin/python experiments/t2m_compare/gen_t2mgpt.py prompts.json out_dir [--repeats 3] [--cpu]

prompts.json as for gen_momask.py; T2M-GPT decides the length itself (it stops at its end token, at most 196 frames
at 20 fps), so "length" is ignored. The model is the released one (pretrained/VQVAE and VQTransformer_corruption05,
the settings of the repository's evaluation command: nb-code 512, down-t 2, depth 3, block-size 51, GPT 9 layers,
16 heads, 1024 wide), sampled with if_categorial=True as in its evaluation, one seed per repeat. Writes
out_dir/<key>_r<repeat>.npy with recover_from_ric joints [T, 22, 3].
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

T2MGPT = Path("/home/jong/baselines/T2M-GPT")


def main() -> int:
    prompts_file, out_dir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    repeats = int(sys.argv[sys.argv.index("--repeats") + 1]) if "--repeats" in sys.argv else 3
    use_cpu = "--cpu" in sys.argv
    prompts = json.loads(prompts_file.read_text())
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(T2MGPT)
    sys.path.insert(0, str(T2MGPT))
    sys.argv = [sys.argv[0]]  # some of the repository's modules parse the command line when imported

    import numpy as np
    import torch
    for alias, value in (("float", float), ("int", int), ("bool", bool), ("object", object)):
        setattr(np, alias, value)  # the repository uses aliases that numpy 1.24 removed
    import clip
    import models.t2m_trans as trans
    import models.vqvae as vqvae
    import options.option_transformer as option_trans
    from utils.motion_process import recover_from_ric

    sys.argv = [sys.argv[0],  # get_args_parser() parses the command line itself
                "--dataname", "t2m", "--nb-code", "512", "--down-t", "2", "--depth", "3", "--block-size", "51",
                "--ff-rate", "4", "--dilation-growth-rate", "3", "--vq-act", "relu", "--quantizer", "ema_reset",
                "--embed-dim-gpt", "1024", "--num-layers", "9", "--n-head-gpt", "16", "--clip-dim", "512"]
    args = option_trans.get_args_parser()
    device = torch.device("cuda" if torch.cuda.is_available() and not use_cpu else "cpu")
    clip_model, _ = clip.load("ViT-B/32", device=device, jit=False)
    if device.type == "cuda":
        clip.model.convert_weights(clip_model)
    clip_model.eval()
    net = vqvae.HumanVQVAE(args, args.nb_code, args.code_dim, args.output_emb_width, args.down_t, args.stride_t,
                           args.width, args.depth, args.dilation_growth_rate)
    trans_encoder = trans.Text2Motion_Transformer(num_vq=args.nb_code, embed_dim=args.embed_dim_gpt,
                                                  clip_dim=args.clip_dim, block_size=args.block_size,
                                                  num_layers=args.num_layers, n_head=args.n_head_gpt,
                                                  drop_out_rate=args.drop_out_rate, fc_rate=args.ff_rate)
    ckpt = torch.load("pretrained/VQVAE/net_last.pth", map_location="cpu", weights_only=False)
    net.load_state_dict(ckpt["net"], strict=True)
    ckpt = torch.load("pretrained/VQTransformer_corruption05/net_best_fid.pth", map_location="cpu", weights_only=False)
    trans_encoder.load_state_dict(ckpt["trans"], strict=True)
    net.eval().to(device)
    trans_encoder.eval().to(device)
    meta = Path("checkpoints/t2m/VQVAEV3_CB1024_CMT_H1024_NRES3/meta")
    mean = torch.from_numpy(np.load(meta / "mean.npy")).to(device)
    std = torch.from_numpy(np.load(meta / "std.npy")).to(device)

    for r in range(repeats):
        torch.manual_seed(1234 + r)
        for p in prompts:
            with torch.no_grad():
                text = clip.tokenize([p["text"]], truncate=True).to(device)
                feat = clip_model.encode_text(text).float()
                index_motion = trans_encoder.sample(feat[0:1], True)
                pose = net.forward_decoder(index_motion)
                joints = recover_from_ric((pose * std + mean).float(), 22)[0].cpu().numpy()
            np.save(out_dir / f"{p['key']}_r{r}.npy", joints.astype(np.float32))
        print(f"repeat {r}: {len(prompts)} motions -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
