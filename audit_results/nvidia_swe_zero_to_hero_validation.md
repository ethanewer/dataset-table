# NVIDIA SWE Zero-to-Hero Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection API for:

- `nvidia/swe-zero-to-swe-hero`

## Coverage

- The collection contains 2 dataset repos.
- Both repos were missing from `datasets.csv` and were added:
  - `nvidia/SWE-Zero-openhands-trajectories`
  - `nvidia/SWE-Hero-openhands-trajectories`

## Row Counts

- `num_rows` uses exact dataset-server `/size` totals:
  - `nvidia/SWE-Zero-openhands-trajectories`: 318,115
  - `nvidia/SWE-Hero-openhands-trajectories`: 34,269

## Classification Decisions

- `is_code_swe_terminal=true` because both datasets are software-engineering agent trajectory datasets for SWE-Bench-style tasks.
- `is_agent=true` because both contain complete OpenHands trajectories with assistant actions and tool/environment observations.
- `is_rl=false` because the released rows are supervised trajectory/patch data, not RL/RLVR prompts, environments, rewards, or verifier-task records.
- `is_pretraining=false` because these are SFT/post-training trajectories, not next-token-prediction corpus data.
- `reasoning=true` because sampled trajectories contain assistant planning/analysis content and OpenHands thought/tool-call traces.

## Verification Columns

- `filtered_for_correctness=false`: the cards describe curated SFT trajectories but do not state that every released trajectory is verified successful.
- `includes_verification=false`: sampled rows expose `instance_id`, `repo`, `license`, `trajectory_id`, `trajectory`, `model_patch`, and `dataset`, with no pass/fail, reward, verifier output, or target-state correctness field.
