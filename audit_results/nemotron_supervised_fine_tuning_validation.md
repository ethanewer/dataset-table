# Nemotron Supervised Fine-Tuning Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection API for:

- `nvidia/nemotron-supervised-fine-tuning`

## Coverage

- The collection contains 38 dataset repos.
- 16 repos were already present in `datasets.csv`.
- Added the 22 missing repos:
  - `nvidia/Nemotron-Math-HumanReasoning`
  - `nvidia/Nemotron-PrismMath`
  - `nvidia/Nemotron-CrossThink`
  - `nvidia/Nemotron-Research-GooseReason-0.7M`
  - `nvidia/AceReason-1.1-SFT`
  - `nvidia/Llama-Nemotron-VLM-Dataset-v1`
  - `nvidia/Nemotron-VLM-Dataset-v2`
  - `nvidia/Nemotron-Cascade-2-SFT-Data`
  - `nvidia/Nemotron-Cascade-SFT-Stage-1`
  - `nvidia/Nemotron-Cascade-SFT-Stage-2`
  - `nvidia/Nemotron-Cascade-SFT-SWE`
  - `nvidia/OpenMathInstruct-1`
  - `nvidia/OpenMathInstruct-2`
  - `nvidia/OpenMath-GSM8K-masked`
  - `nvidia/OpenMath-MATH-masked`
  - `nvidia/Nemotron-Personas-USA`
  - `nvidia/Nemotron-Personas-Brazil`
  - `nvidia/Nemotron-Personas-France`
  - `nvidia/Nemotron-Personas-India`
  - `nvidia/Nemotron-Personas-Japan`
  - `nvidia/Nemotron-Personas-Korea`
  - `nvidia/Nemotron-Personas-Singapore`

## Row Counts

- Used exact dataset-server `/size` totals when the viewer returned complete rows.
- Used dataset-card totals when dataset-server was preview-only or partial and the card exposed fuller public statistics.
- Used dataset-server totals for `nvidia/Nemotron-Cascade-SFT-SWE` and `nvidia/OpenMathInstruct-1` because the current server rows are higher than the collection estimates and match the currently materialized dataset.
- Used card totals for `nvidia/AceReason-1.1-SFT`, `nvidia/Nemotron-VLM-Dataset-v2`, `nvidia/Nemotron-Cascade-2-SFT-Data`, and the Cascade stage blends where public card totals were more complete than partial dataset-server estimates.

## Classification Decisions

- `is_pretraining=false` for all newly added rows because the collection is post-training/SFT/RL task data rather than primarily next-token-prediction corpus data.
- `is_rl=true` for:
  - `nvidia/Nemotron-CrossThink`, which exposes `reward_model` ground-truth/evaluation style fields.
  - `nvidia/Nemotron-Research-GooseReason-0.7M`, which is described as an RLVR task dataset and releases multiple-choice tasks with correct answers.
- `is_agent=true` for:
  - `nvidia/Nemotron-Cascade-2-SFT-Data`, because it includes conversational-agent, SWE-agent, and terminal-agent domains.
  - `nvidia/Nemotron-Cascade-SFT-Stage-2`, because it includes tool-calling data.
- `is_code_swe_terminal=true` only for `nvidia/Nemotron-Cascade-SFT-SWE`, which is dedicated SWE code repair/localization/test-generation data.
- Mixed math/code datasets such as `nvidia/AceReason-1.1-SFT`, `nvidia/OpenMathInstruct-1`, and `nvidia/Nemotron-Research-GooseReason-0.7M` were not marked code because code is not the primary dataset purpose under the current schema.
- Math datasets with Python/tool use were not marked code/SWE/terminal.
- Persona and VLM datasets were not marked agent, RL, code, SWE, terminal, or pretraining.

## Verification Columns

- Agent/RL rows use `filtered_for_correctness=false` unless the release is explicitly filtered to only verified successful completions.
- RL task rows with answer/reward targets use `includes_verification=true`.
- Agent SFT rows without released pass/fail, reward, or target-state fields use `includes_verification=false`.
- Non-agent, non-RL rows keep `filtered_for_correctness` and `includes_verification` blank.
