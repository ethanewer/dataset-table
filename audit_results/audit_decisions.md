# Dataset Table Audit Decisions

This audit was run with `run_row_audits.py`, which launched one headless Codex CLI worker per CSV row. Each worker wrote a structured row audit to `audit_results/<row>_<dataset>.json` and an event/source log to the matching `.events.jsonl` file.

## Applied Corrections

| Row | Dataset | Corrections applied |
|---:|---|---|
| 1 | `nvidia/Nemotron-SFT-Math-v3` | `teacher_model` now includes both `DeepSeek-V3.2-Speciale` and `DeepSeek-V3.2`; `reasoning` is aligned as `[true,true]`; `DeepSeek-V3.2` was removed from `aux_models` because it is a teacher for TIR solution generation. |
| 2 | `nvidia/Nemotron-SFT-Multilingual-v1` | `is_code_swe_terminal=false`; code is present but not the primary dataset scope under the schema. |
| 4 | `nvidia/Nemotron-Math-Proofs-v1` | `is_code_swe_terminal=false`; Lean/formal-proof data is not treated as code/SWE/terminal for this table unless the dataset is actually coding, SWE, shell, terminal, or agentic coding oriented. Agent/RL-only fields were left unchanged because this is neither an agent-rollout nor RL dataset. |
| 6 | `nvidia/Nemotron-SFT-OpenCode-v1` | `num_rows=460254` from the exact manifest total. |
| 9 | `nvidia/Nemotron-SFT-Agentic-v2` | `includes_verification=true` because released rows expose target/correct-answer fields; `aux_models` now records the named LLM judges `DeepSeek-V3.2` and `GLM-4.6`. |
| 10 | `nvidia/Nemotron-Science-v1` | `teacher_model` now captures MCQ and RQA sources as `["GPT-OSS-120B","not_specified"]`; `reasoning` is aligned as `[true,true]`; `aux_models=[]`. |
| 13 | `allenai/Dolci-Think-SFT-7B` | `is_code_swe_terminal=false`; `teacher_model` now includes `QwQ-32B`; `reasoning` is aligned as `[true,true,true]`; `aux_models` records GPT-4.1 test-case generation/filtering. |
| 17 | `open-thoughts/AgentTrove` | `aux_models` now records `GPT-4o-mini` judging from a linked source dataset. |

## Reviewed But Not Applied

| Row | Dataset | Row-agent suggestion not applied | Reason |
|---:|---|---|---|
| 4 | `nvidia/Nemotron-Math-Proofs-v1` | Mark `is_agent=true`, `filtered_for_correctness=true`, and `includes_verification=false`. | The schema defines `is_agent` as agent rollouts or trajectories. Lean proof-generation/proof-code data is verified SFT data, but not an agent rollout dataset. Agent/RL-only verification columns stay blank for datasets that are neither agent nor RL. |

## Remaining Uncertainties

The row agents marked `already_included` as uncertain for many rows because that field is internal provenance from the Slack thread/current training set, not public dataset metadata. I left it governed by the user-provided Slack context: original/current datasets stay `true`, later additions stay `false`.
