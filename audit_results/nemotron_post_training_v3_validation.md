# Nemotron Post-Training v3 Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection API for:

- `nvidia/nemotron-post-training-v3`

## Coverage

- The collection contains 28 dataset repos.
- 11 repos were already present in `datasets.csv`.
- Added the 17 missing repos:
  - `nvidia/Nemotron-3-Nano-RL-Training-Blend`
  - `nvidia/Nemotron-Agentic-v1`
  - `nvidia/Nemotron-Competitive-Programming-v1`
  - `nvidia/Nemotron-Math-v2`
  - `nvidia/Nemotron-SWE-v1`
  - `nvidia/Nemotron-SpecializedDomains-Finance-v1`
  - `nvidia/Nemotron-RLHF-GenRM-v1`
  - `nvidia/Nemotron-RL-ReasoningGym-v1`
  - `nvidia/Nemotron-RL-Safety-v1`
  - `nvidia/Nemotron-RL-Identity-Following-v1`
  - `nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1`
  - `nvidia/Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1`
  - `nvidia/Nemotron-RL-Agentic-Function-Calling-Pivot-v1`
  - `nvidia/Nemotron-RL-Instruction-Following-Adversarial-v1`
  - `nvidia/Nemotron-RL-Instruction-Following-MultiTurnChat-v1`
  - `nvidia/Nemotron-RL-Instruction-Following-Calendar-v2`
  - `nvidia/Nemotron-RL-Super-Training-Blends`

## Row Counts

- Used exact dataset-server `/size` totals where the viewer returned a complete row count.
- Used dataset-card totals when dataset-server reported `0` for preview repos.
- For partial dataset-server rows with public card totals, used the card total when the server explicitly showed it had only materialized a partial view.
- `nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1` is the exception: the card's `6,436` sample count appears stale relative to the current file and dataset-server schema, so `num_rows=50308` uses the current dataset-server row count.

## Classification Decisions

- `is_pretraining=false` for all new rows because this collection is post-training data, not primarily next-token-prediction corpus data.
- `is_rl=true` for the NeMo Gym/RLVR/RLHF datasets and training blends.
- `is_agent=true` for tool-use, function-calling, SWE, and mixed training blends that include agent/tool/SWE components.
- `is_code_swe_terminal=true` only for rows primarily about competitive programming or SWE agent tasks:
  - `nvidia/Nemotron-Competitive-Programming-v1`
  - `nvidia/Nemotron-SWE-v1`
  - `nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1`
- Broad RL blends were not marked as code/SWE/terminal because code/SWE is only one component of the blend.
- Math and finance reasoning datasets were not marked as code/SWE/terminal, even when they include Python tool use or structured reasoning.

## Verification Columns

- Agent/RL rows use `filtered_for_correctness=false` unless the released rows are explicitly all verified successful completions.
- Agent/RL rows use `includes_verification=true` when rows expose expected actions, rubrics, pass rates, rankings, reference states, rewards, or other verifier targets.
- Non-agent, non-RL rows keep `filtered_for_correctness` and `includes_verification` blank.
