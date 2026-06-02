# Current Datasets CSV Schema

This document defines the columns in `datasets.csv`. All values are stored as CSV strings; the `Type` column below describes the intended semantic type.

| Column | Type | Description |
|---|---:|---|
| `dataset_name` | string | Hugging Face dataset repo id, e.g. `nvidia/Nemotron-Terminal-Corpus`. |
| `dataset_url` | string | Public Hugging Face dataset URL. |
| `is_code_swe_terminal` | boolean | `true` if the dataset is primarily code, software engineering, shell, terminal, or agentic coding related. |
| `is_agent` | boolean | `true` if the dataset contains agent rollouts, trajectories, tool-use traces, terminal/computer-use traces, or equivalent agent interaction data. This includes supervised traces, mid-training trace corpora, and completed agent rollouts; it is not limited to final SFT recipes. |
| `is_rl` | boolean | `true` if the dataset contains RL/RLVR prompts, tasks, environments, rewards, verifier targets, or rollout-selection metadata. This is independent of whether the dataset is agentic. |
| `is_pretraining` | boolean | `true` if the dataset is primarily next-token-prediction pretraining data, such as raw or synthetic text/code/math corpora. Use `false` for datasets that are mainly LLM conversations, SFT, DPO, RL prompts, or agent trajectories, even if they are used during a broader pretraining release. |
| `reasoning` | boolean or JSON list string | `true` if inspected samples include reasoning in any form: `reasoning_content`, `<think>` tags, a dedicated reasoning/thinking field, or explicit assistant `analysis`/`plan`/`THOUGHT` content. If `teacher_model` is a JSON list, this is a same-length JSON boolean list aligned by position to `teacher_model`; each element states whether traces from that teacher/source include explicit reasoning. |
| `filtered_for_correctness` | boolean/null | Agent/RL-only. `true` only if the released dataset is filtered so all included trajectories or rollout/task records are verified successful, equivalent to `reward=1` or passing the task verifier. `false` if failed/incomplete trajectories remain or if there is no evidence that all records are verified successful. Blank for datasets that are neither agent nor RL. |
| `includes_verification` | boolean/null | Agent/RL-only. `true` if the released dataset contains a non-empty pass/fail, reward, target, verifier output, ground-truth answer, or equivalent correctness field. `false` if tests/verifiers may exist for the underlying tasks but the released rows do not include correctness results or targets. Blank for datasets that are neither agent nor RL. |
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
- `filtered_for_correctness` is stricter than general quality filtering. LLM judging, heuristic filtering, deduplication, or format filtering does not make it `true` unless the remaining trajectories or rollout/task records are all verified task completions.
- `includes_verification=true` does not imply the dataset is filtered to only successful trajectories; it only means pass/fail-style information is present.
