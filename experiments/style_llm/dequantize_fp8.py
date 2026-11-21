#!/home/jong/isaaclab/.venv/bin/python
"""Write a bf16 copy of a block-wise FP8 Qwen3 checkpoint, so it can be loaded in 4 bit (bitsandbytes) instead.

Usage on this computer:
    ./experiments/style_llm/dequantize_fp8.py <FP8 snapshot dir> /home/jong/models/Qwen3-8B-from-FP8

The FP8 kernels of this GPU's triton (3.3, compute capability 12.0) are missing, so the FP8 checkpoint cannot run
here (2026-11-05). Each FP8 weight is multiplied by its per-block scale (weight_scale_inv, 128 x 128 blocks), which
is exactly what the FP8 kernel does before its matmul; the copy has the FP8 checkpoint's values in bf16.
"""

import json
import shutil
import sys
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    config = json.loads((src / "config.json").read_text())
    block = config.pop("quantization_config")["weight_block_size"]
    index = json.loads((src / "model.safetensors.index.json").read_text())
    weight_map = {}
    for shard in sorted(set(index["weight_map"].values())):
        tensors = load_file(src / shard)
        out = {}
        for name, tensor in tensors.items():
            if name.endswith("_scale_inv"):
                continue
            scale = tensors.get(name + "_scale_inv")
            if scale is not None:
                rows, cols = tensor.shape
                scale = scale.float().repeat_interleave(block[0], 0)[:rows].repeat_interleave(block[1], 1)[:, :cols]
                tensor = (tensor.float() * scale).to(torch.bfloat16)
            out[name] = tensor.contiguous()
            weight_map[name] = shard
        save_file(out, dst / shard, metadata={"format": "pt"})
        print(shard, len(out), "tensors", flush=True)
    (dst / "config.json").write_text(json.dumps(config, indent=2))
    (dst / "model.safetensors.index.json").write_text(json.dumps({"metadata": {}, "weight_map": weight_map}, indent=2))
    for name in ("generation_config.json", "tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt",
                 "LICENSE"):
        shutil.copy(src / name, dst / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
