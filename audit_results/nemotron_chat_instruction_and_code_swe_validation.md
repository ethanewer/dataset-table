# Nemotron Chat/Instruction and Code/SWE Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection APIs for:

- `nvidia/nemotron-chat-and-instruction-following`
- `nvidia/nemotron-code-and-swe`

## Coverage

- `nvidia/nemotron-chat-and-instruction-following` contains 11 dataset repos.
- 7 chat/instruction repos were already present in `datasets.csv`.
- Added the 4 missing chat/instruction repos:
  - `nvidia/Nemotron-RL-instruction_following`
  - `nvidia/Nemotron-RL-instruction_following-structured_outputs`
  - `nvidia/Nemotron-Cascade-RL-Instruction-Following`
  - `nvidia/HelpSteer3`
- `nvidia/nemotron-code-and-swe` contains 12 dataset repos.
- 10 code/SWE repos were already present in `datasets.csv`.
- Added the 2 missing code/SWE repos:
  - `nvidia/Nemotron-RL-coding-competitive_coding`
  - `nvidia/Nemotron-Cascade-RL-SWE`

## Row Counts

- Used exact dataset-server `/size` totals where complete:
  - `nvidia/Nemotron-RL-instruction_following-structured_outputs`: 9,949
  - `nvidia/Nemotron-Cascade-RL-Instruction-Following`: 108,938
  - `nvidia/HelpSteer3`: 132,937
  - `nvidia/Nemotron-RL-coding-competitive_coding`: 16,083
- Used the dataset card count for `nvidia/Nemotron-RL-instruction_following` because dataset-server reports `0` rows while the card states 46,391 records.
- Used 109,996 for `nvidia/Nemotron-Cascade-RL-SWE` because the collection API and dataset-server estimate report 109,996 while the materialized dataset-server view is partial at 27,369 rows.
- No archive expansion, bulk dataset download, or row-content streaming was used.

## Classification Decisions

- All newly added rows are post-training/alignment data, so `is_pretraining=false`.
- `is_rl=true` for all six new rows because they are RLVR, IF-RL, reward-model, preference, or RL SWE training datasets.
- `is_agent=false` for all six new rows:
  - Instruction-following and structured-output rows are verifiable RL tasks, not agent trajectories.
  - `nvidia/Nemotron-Cascade-RL-SWE` is SWE repair RL data, but the card describes an agentless mini framework and no execution-based reward.
  - `nvidia/HelpSteer3` is mixed-domain preference/feedback data rather than agent rollout data.
- `is_code_swe_terminal=true` only for the two code/SWE additions:
  - `nvidia/Nemotron-RL-coding-competitive_coding`
  - `nvidia/Nemotron-Cascade-RL-SWE`
- `nvidia/HelpSteer3` includes code-domain examples but is not marked code/SWE/terminal because its primary scope is mixed-domain reward/preference alignment.

## Verification Columns

- `includes_verification=true` for the new RL rows because they expose verifiable constraints, schema targets, rule-verifier metadata, preference labels, unit tests, golden patches, or reward-model targets.
- `filtered_for_correctness=false` for the new RL rows because none of the cards state that released samples are only verified successful completions.
- `nvidia/HelpSteer3` records `DeepSeek V3` in `aux_models` for principle generation.
- `nvidia/Nemotron-Cascade-RL-SWE` records `Kimi-Dev-72B` in `aux_models` for execution-free reward modeling.
