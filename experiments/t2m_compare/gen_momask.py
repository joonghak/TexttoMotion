"""MoMask (Guo et al., CVPR 2024) on our commands: the joints the model generates, saved without post-processing.

Usage on this computer (MoMask's own environment, run from anywhere):
    /home/jong/baselines/venv/bin/python experiments/t2m_compare/gen_momask.py prompts.json out_dir [--repeats 3] [--cpu]

prompts.json: [{"key": "set8_Q1", "text": "A person walks ...", "length": 196}, ...] (length in frames at 20 fps,
rounded down to a multiple of 4; 196 is the longest HumanML3D clip). Writes out_dir/<key>_r<repeat>.npy with the
joint positions [T, 22, 3] that MoMask's own gen_t2m.py computes with recover_from_ric, before its BVH conversion
and foot IK (gen_t2m.py saves the joints after the BVH round trip and after drawing an animation, which needs an
older matplotlib). Model loading, sampling settings and the seed are those of gen_t2m.py (EvalT2MOptions defaults).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

MOMASK = Path("/home/jong/baselines/momask-codes")


def main() -> int:
    prompts_file, out_dir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    repeats = int(sys.argv[sys.argv.index("--repeats") + 1]) if "--repeats" in sys.argv else 3
    use_cpu = "--cpu" in sys.argv  # when the GPU is taken by a training
    prompts = json.loads(prompts_file.read_text())
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(MOMASK)
    sys.path.insert(0, str(MOMASK))
    sys.argv = [sys.argv[0], "--gpu_id", "0", "--ext", "ours_compare"]

    from os.path import join as pjoin

    import numpy as np
    import torch
    for alias, value in (("float", float), ("int", int), ("bool", bool), ("object", object)):
        setattr(np, alias, value)  # the repository (2023) uses aliases that numpy 1.24 removed
    from models.mask_transformer.transformer import MaskTransformer, ResidualTransformer
    from models.vq.model import RVQVAE
    from options.eval_option import EvalT2MOptions
    from utils.fixseed import fixseed
    from utils.get_opt import get_opt
    from utils.motion_process import recover_from_ric

    clip_version = "ViT-B/32"

    def load(path, device="cpu"):  # the authors' checkpoints hold option objects next to the weights
        return torch.load(path, map_location=device, weights_only=False)

    # the loaders of gen_t2m.py, which cannot be imported here: its visualization imports need numpy.core.umath_tests
    class g:
        @staticmethod
        def load_vq_model(vq_opt):
            model = RVQVAE(vq_opt, vq_opt.dim_pose, vq_opt.nb_code, vq_opt.code_dim, vq_opt.output_emb_width,
                           vq_opt.down_t, vq_opt.stride_t, vq_opt.width, vq_opt.depth, vq_opt.dilation_growth_rate,
                           vq_opt.vq_act, vq_opt.vq_norm)
            ckpt = load(pjoin(vq_opt.checkpoints_dir, vq_opt.dataset_name, vq_opt.name, "model", "net_best_fid.tar"))
            model.load_state_dict(ckpt["vq_model" if "vq_model" in ckpt else "net"])
            return model, vq_opt

        @staticmethod
        def load_trans_model(model_opt, opt, which_model):
            model = MaskTransformer(code_dim=model_opt.code_dim, cond_mode="text", latent_dim=model_opt.latent_dim,
                                    ff_size=model_opt.ff_size, num_layers=model_opt.n_layers,
                                    num_heads=model_opt.n_heads, dropout=model_opt.dropout, clip_dim=512,
                                    cond_drop_prob=model_opt.cond_drop_prob, clip_version=clip_version, opt=model_opt)
            ckpt = load(pjoin(model_opt.checkpoints_dir, model_opt.dataset_name, model_opt.name, "model", which_model))
            missing, unexpected = model.load_state_dict(ckpt["t2m_transformer" if "t2m_transformer" in ckpt else "trans"],
                                                        strict=False)
            assert not unexpected and all(k.startswith("clip_model.") for k in missing)
            return model

        @staticmethod
        def load_res_model(res_opt, vq_opt, opt):
            res_opt.num_quantizers = vq_opt.num_quantizers
            res_opt.num_tokens = vq_opt.nb_code
            model = ResidualTransformer(code_dim=vq_opt.code_dim, cond_mode="text", latent_dim=res_opt.latent_dim,
                                        ff_size=res_opt.ff_size, num_layers=res_opt.n_layers, num_heads=res_opt.n_heads,
                                        dropout=res_opt.dropout, clip_dim=512, shared_codebook=vq_opt.shared_codebook,
                                        cond_drop_prob=res_opt.cond_drop_prob, share_weight=res_opt.share_weight,
                                        clip_version=clip_version, opt=res_opt)
            ckpt = load(pjoin(res_opt.checkpoints_dir, res_opt.dataset_name, res_opt.name, "model", "net_best_fid.tar"))
            missing, unexpected = model.load_state_dict(ckpt["res_transformer"], strict=False)
            assert not unexpected and all(k.startswith("clip_model.") for k in missing)
            return model

    opt = EvalT2MOptions().parse()
    fixseed(opt.seed)
    opt.device = torch.device("cuda:0" if torch.cuda.is_available() and not use_cpu else "cpu")
    dim_pose = 263
    root_dir = pjoin(opt.checkpoints_dir, opt.dataset_name, opt.name)
    model_opt = get_opt(pjoin(root_dir, "opt.txt"), device=opt.device)
    vq_opt = get_opt(pjoin(opt.checkpoints_dir, opt.dataset_name, model_opt.vq_name, "opt.txt"), device=opt.device)
    vq_opt.dim_pose = dim_pose
    vq_model, vq_opt = g.load_vq_model(vq_opt)
    model_opt.num_tokens = vq_opt.nb_code
    model_opt.num_quantizers = vq_opt.num_quantizers
    model_opt.code_dim = vq_opt.code_dim
    res_opt = get_opt(pjoin(opt.checkpoints_dir, opt.dataset_name, opt.res_name, "opt.txt"), device=opt.device)
    res_model = g.load_res_model(res_opt, vq_opt, opt)
    t2m_transformer = g.load_trans_model(model_opt, opt, "latest.tar")
    for model in (t2m_transformer, vq_model, res_model):
        model.eval()
        model.to(opt.device)
    mean = np.load(pjoin(opt.checkpoints_dir, opt.dataset_name, model_opt.vq_name, "meta", "mean.npy"))
    std = np.load(pjoin(opt.checkpoints_dir, opt.dataset_name, model_opt.vq_name, "meta", "std.npy"))

    captions = [p["text"] for p in prompts]
    token_lens = torch.LongTensor([int(p.get("length", 196)) // 4 for p in prompts]).to(opt.device)
    for r in range(repeats):
        fixseed(opt.seed + r)
        with torch.no_grad():
            mids = t2m_transformer.generate(captions, token_lens, timesteps=opt.time_steps, cond_scale=opt.cond_scale,
                                            temperature=opt.temperature, topk_filter_thres=opt.topkr,
                                            gsample=opt.gumbel_sample)
            mids = res_model.generate(mids, captions, token_lens, temperature=1, cond_scale=5)
            motions = vq_model.forward_decoder(mids).detach().cpu().numpy() * std + mean
        for p, motion, n in zip(prompts, motions, (token_lens * 4).tolist()):
            joints = recover_from_ric(torch.from_numpy(motion[:n]).float(), 22).numpy()
            np.save(out_dir / f"{p['key']}_r{r}.npy", joints.astype(np.float32))
        print(f"repeat {r}: {len(prompts)} motions -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
