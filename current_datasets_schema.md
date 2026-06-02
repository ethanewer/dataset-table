# Current Datasets CSV Schema

This document defines the columns in `current_datasets.csv`. All values are stored as CSV strings; the `Type` column below describes the intended semantic type.

| Column | Type | Description |
|---|---:|---|
| `dataset_name` | string | Hugging Face dataset repo id, e.g. `nvidia/Nemotron-Terminal-Corpus`. |
| `dataset_url` | string | Public Hugging Face dataset URL. |
| `is_code_swe_terminal` | boolean | `true` if the dataset is primarily code, software engineering, shell, terminal, or agentic coding related. |
| `is_agent_sft` | boolean | `true` if the dataset contains supervised agent rollouts or trajectories. This can include SFT, mid-training, or trace corpora; it is not limited to final SFT recipes. |
| `is_agent_rl` | boolean | `true` if the dataset contains RL environments/tasks/verifiers rather than only completed traces. |
| `reasoning` | boolean or JSON list string | `true` if inspected samples include reasoning in any form: `reasoning_content`, `<think>` tags, a dedicated reasoning/thinking field, or explicit assistant `analysis`/`plan`/`THOUGHT` content. If `teacher_model` is a JSON list, this is a same-length JSON boolean list aligned by position to `teacher_model`; each element states whether traces from that teacher/source include explicit reasoning. |
| `filtered_for_correctness` | boolean/null | Agent-only. `true` only if the released dataset is filtered so all included agent trajectories are verified successful, equivalent to `reward=1` or passing the task verifier. `false` if failed/incomplete trajectories remain or if there is no evidence that all trajectories are verified successful. Blank for non-agent datasets. |
| `includes_verification` | boolean/null | Agent-only. `true` if the released dataset contains a non-empty pass/fail, reward, target, verifier output, or equivalent correctness field for trajectories. `false` if tests/verifiers may exist for the underlying tasks but the released rows do not include trajectory-level correctness results. Blank for non-agent datasets. |
| `teacher_model` | string or JSON list string | Model that generated the synthetic data or trajectories. If multiple teacher models are used, this is a JSON list string such as `["model_a", "model_b"]`. Use `not_specified` when no source identifies the teacher. |
| `aux_models` | JSON array string | Additional models used for related model-driven steps, such as user simulation, judging, post-editing, or skill generation. Format: `[{"model":"...","use":"..."}]`. Use `[]` when none are known. Do not put non-model tooling or frameworks here. |
| `agent_harness` | string or JSON list string | Agent harness used for trajectory generation, e.g. `Terminus-2`, `OpenHands`, `SWE-agent`, `pi`. If multiple actual harnesses are used, this is a JSON list string. Do not include data-generation frameworks or tooling unless they are the harness. |
| `num_rows` | integer | Dataset row count. Prefer Hugging Face dataset-server exact totals when available; otherwise use the dataset card’s stated total. Rounded card totals are recorded as rounded integers and should be treated as approximate. |
| `already_included` | boolean | `true` for datasets that were already included in the original Slack thread/current training set; `false` for later candidate additions. |

## Value Conventions

- Booleans are lowercase CSV strings: `true` or `false`.
- Null values are blank cells.
- JSON-list strings must be valid JSON, even inside CSV quoting.
- If `teacher_model` is a JSON list, `reasoning` must also be a JSON list of booleans with the same length and order.
- `agent_harness` is blank for non-agent datasets or when no named harness is identified.
- `filtered_for_correctness` is stricter than general quality filtering. LLM judging, heuristic filtering, deduplication, or format filtering does not make it `true` unless the remaining trajectories are all verified task completions.
- `includes_verification=true` does not imply the dataset is filtered to only successful trajectories; it only means pass/fail-style information is present.
