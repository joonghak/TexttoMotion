# Third-party source: MimicKit

- Upstream: https://github.com/xbpeng/MimicKit
- Imported directory: `MimicKit/`
- Branch at import: `main`
- Commit: `2ed1e6c093bb0829f55d33cb4f7a1731cfe6cb69`
- Commit date: `2026-06-23T10:18:29-07:00`
- Import date: `2026-09-06`
- License: [Apache-2.0](MimicKit/LICENSE)
- Copyright: Xue Bin Peng, 2025

The directory contains the upstream tracked source files at the commit above,
exported with `git archive`. It is a normal directory in this repository, not a
Git submodule. No upstream source modifications were made during the import itself.

## Modifications for TexttoMotion

- `MimicKit/mimickit/envs/text_reward_env.py` (added): the imitation reward with style targets set from a text command.
- `MimicKit/mimickit/envs/env_builder.py`: registers the `text_reward` environment.
- `MimicKit/mimickit/learning/base_agent.py`, `MimicKit/mimickit/run.py`: optional checkpoints at given iterations
  (`checkpoint_iters`).

Each modified file carries a one-line notice at its top.

When distributing modifications, retain the license and attribution notices,
and mark modified upstream files as required by the Apache-2.0 license.
External motion datasets, pretrained models, and simulator dependencies may
have separate terms; importing this source does not grant rights to those assets.

For research use, cite the relevant methods (including DeepMimic when used) and
the MimicKit framework as described in the upstream documentation.

# Third-party data: 100STYLE (evaluation only)

- Source: https://www.ianxmason.com/100style (Zenodo record https://zenodo.org/record/8127870)
- Used: the 100 forward-walk BVH files (`<Style>_FW.bvh`) and `Frame_Cuts.csv`, downloaded on 2026-11-05 to
  `/home/jong/datasets/100STYLE/` (outside this repository; not redistributed here)
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Attribution: "The 100STYLE Dataset - Ian Mason"; cite Mason, Starke and Komura, "Real-Time Style Modelling of
  Human Locomotion via Feature-Wise Transformations and Local Motion Phases", 2022
- Use in this repository: gait features measured from the motion capture serve as the reference of the style metric
  (`experiments/style_eval/`). The clips are not used as reference motions for training, and our reward formula is
  not applied to them. `experiments/style_eval/reference_100style.json` holds only derived feature values.
