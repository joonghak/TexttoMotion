"""Style similarity of one of our walks to the 100STYLE styles.

A walk is described by its style difference (gait_features.style_delta): how its gait features differ from the
plain walk of the same skeleton. Each feature is divided by its spread over the 99 100STYLE styles, so that every
feature counts about equally. For a walk aimed at a 100STYLE style the metric gives:
    similarity  cosine between our difference and the style's difference (+1 same direction of change, 0 unrelated)
    rank        place of the aimed style among the 99 styles ordered by similarity (1 = the most similar)
    strength    length of our difference / length of the style's difference (1 = as strong as the motion capture)
Rank is the style-recognition idea of SMooDi (Zhong et al. 2024), which classifies generated motions into
100STYLE styles, with these gait features and nearest-style ranking in place of a trained classifier.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "reference_100style.json"


class Reference:
    def __init__(self, path: Path = REFERENCE):
        data = json.loads(path.read_text())
        self.features = list(data["features"])
        self.scale = np.array([data["scale"][name] for name in self.features])
        self.names = [name for name, entry in data["styles"].items() if entry["delta"] is not None]
        self.deltas = np.array([[data["styles"][name]["delta"][f] for f in self.features] for name in self.names],
                               dtype=float) / self.scale
        self.raw = data

    def scaled(self, delta: np.ndarray) -> np.ndarray:
        return np.asarray(delta, dtype=float) / self.scale

    def similarities(self, delta: np.ndarray, use: list | None = None) -> np.ndarray:
        """Cosine of our scaled difference with every style's, over the features both have (and in use, if given)."""
        ours = self.scaled(delta)
        mask = np.isfinite(ours)[None, :] & np.isfinite(self.deltas)
        if use is not None:
            mask &= np.isin(self.features, use)[None, :]
        a = np.where(mask, ours[None, :], 0.0)
        b = np.where(mask, self.deltas, 0.0)
        return np.sum(a * b, axis=1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1) + 1e-12)

    def evaluate(self, delta: np.ndarray, target: str | None = None, top: int = 5, use: list | None = None) -> dict:
        sims = self.similarities(delta, use)
        order = np.argsort(-sims)
        result = {"top": [(self.names[i], round(float(sims[i]), 3)) for i in order[:top]]}
        if target is not None:
            t = self.names.index(target)
            ours, ref = self.scaled(delta), self.deltas[t]
            mask = np.isfinite(ours) & np.isfinite(ref)
            result.update(similarity=round(float(sims[t]), 3),
                          rank=int(np.nonzero(order == t)[0][0]) + 1,
                          strength=round(float(np.linalg.norm(ours[mask]) / np.linalg.norm(ref[mask])), 3))
        return result
