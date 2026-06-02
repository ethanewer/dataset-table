# Split Datasets CSV Schema

This document defines `split_datasets.csv`, the split-level expansion of `datasets.csv`.

Each row is keyed by:

- `dataset_name`
- `dataset_config`
- `split`

The config is required because many Hugging Face datasets reuse split names such as `train` across multiple configs.

| Column | Type | Description |
|---|---:|---|
| `dataset_name` | string | Hugging Face dataset repo id. |
| `dataset_config` | string | Hugging Face dataset config name. Use `default` when no named config is exposed. |
| `split` | string | Hugging Face split name for the config. |
| `dataset_url` | string | Public Hugging Face dataset URL. |
| `split_url` | string | Hugging Face dataset URL with `config` and `split` query parameters. |
| `is_code_swe_terminal` | boolean | Split-level classification for code, SWE, shell, terminal, or agentic coding data. Mixed parent datasets can have both true and false split rows. |
| `is_agent` | boolean | Split-level classification for agent rollouts, trajectories, tool-use traces, terminal/computer-use traces, or equivalent agent interaction data. Agentless splits are false even when another split in the same dataset is agentic. |
| `is_rl` | boolean | Split-level RL/RLVR/RLHF classification. Inherits the parent value unless the split metadata clearly narrows the classification. |
| `is_pretraining` | boolean | Split-level next-token-prediction pretraining classification. |
| `reasoning` | boolean or JSON list string | Split-level reasoning classification. For explicit `reasoning_on` and `reasoning_off` splits this is scalar true/false. Otherwise it follows the parent row convention. |
| `filtered_for_correctness` | boolean/null | Agent/RL-only at split level. Blank for splits that are neither agent nor RL. |
| `includes_verification` | boolean/null | Agent/RL-only at split level. Blank for splits that are neither agent nor RL. |
| `teacher_model` | string or JSON list string | Model that generated the synthetic data or trajectories, inherited from the parent dataset unless split-specific evidence is available. |
| `aux_models` | JSON array string | Additional models used for judging, post-editing, reward modeling, or related model-driven steps. |
| `agent_harness` | string or JSON list string | Split-level agent harness. Blank for non-agent splits. |
| `num_rows` | integer/null | Split row count when Hugging Face dataset-server or the dataset card exposes a count. Blank when split-level counts are not public without counting dataset files. |
| `num_rows_source` | string | Source/precision for `num_rows`: `dataset_server_exact`, `dataset_server_partial`, `dataset_server_estimated`, `dataset_card_exact`, `parent_single_split`, or `not_public_per_split`. |
| `parent_num_rows` | integer | The dataset-level row count from `datasets.csv`. |
| `already_included` | boolean | Inherited from the parent dataset row. |

## Validation

Run:

```bash
python3 generate_split_datasets.py
python3 audit_split_datasets.py
```

The audit verifies schema shape, unique split keys, Hugging Face split coverage, count sources, JSON cells, boolean cells, and split-specific classification rules such as `agentless` versus `openhands_swe`.
