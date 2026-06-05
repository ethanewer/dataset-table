# Condensed Split Datasets CSV Schema

`condensed_split_datasets.csv` is a regex-compressed view of `split_datasets.csv`.

Each row represents one or more source rows. A source row is covered when:

- `dataset_name` fully matches `dataset_name_regex`
- `hf_split` fully matches `hf_split_regex`
- `dataset_config` fully matches `dataset_config_regex`
- all condensed metadata columns match exactly

| Column | Type | Description |
|---|---:|---|
| `readable_name` | string | Compact human-readable label for the regex row. Unique within the condensed CSV and at most 64 characters. |
| `dataset_name_regex` | regex string | Full-match regex over `split_datasets.csv.dataset_name`. |
| `hf_split_regex` | regex string | Full-match regex over `split_datasets.csv.hf_split`. |
| `dataset_config_regex` | regex string | Full-match regex over `split_datasets.csv.dataset_config`. |
| `is_code_swe_terminal` | boolean | Shared metadata value for all covered source rows. |
| `is_agent` | boolean | Shared metadata value for all covered source rows. |
| `is_rl` | boolean | Shared metadata value for all covered source rows. |
| `is_pretraining` | boolean | Shared metadata value for all covered source rows. |
| `reasoning` | boolean or JSON list string | Shared metadata value for all covered source rows. |
| `teacher_model` | string or JSON list string | Shared metadata value for all covered source rows. |
| `aux_models` | JSON array string | Shared metadata value for all covered source rows. |
| `agent_harness` | string or JSON list string | Shared metadata value for all covered source rows. |
| `already_included` | boolean | Shared metadata value for all covered source rows. |
| `num_rows_total` | integer/null | Sum of covered source `num_rows` values when all are public integers. For selected `not_public_per_split` rows, this is a best-available estimate from parent row counts, exact dataset-card totals, or parent counts weighted by repository file sizes. Blank only when no usable exact or estimated total is available. |
| `num_rows_source` | string | Shared source-row `num_rows_source` value for all covered source rows. When this is `not_public_per_split` and `num_rows_total` is populated, the total is estimated or parent-derived rather than a public split-level count. |
| `covered_rows` | integer | Number of `split_datasets.csv` rows covered by this regex row. |
| `downloaded` | boolean | True only when all covered split rows are marked downloaded. |
| `local_path` | string or JSON list string/null | Shared local path when all covered split rows use one path; otherwise a JSON list of known local paths. Paths are blank when no local path is known. |
| `qwen_estimated_tokens` | integer/null | Sum of covered split-level Qwen token estimates when every covered split has an estimate. |
| `nemotron_estimated_tokens` | integer/null | Sum of covered split-level Nemotron token estimates when every covered split has an estimate. |
| `avg_estimated_tokens` | integer/null | Sum of covered split-level average token estimates when every covered split has an estimate. |
| `token_estimate_method` | string/null | Single split-level method for one-row groups, or `aggregate_from_split_estimates` for multi-row groups with estimates. |
| `token_estimate_sample_rows` | integer/null | Sum of covered split-level sample-row counts when every covered split has a value. |
| `token_estimate_notes` | string/null | Single split-level estimate note for one-row groups, or an aggregate note for multi-row groups with estimates. |

## Validation

Run:

```bash
python3 generate_condensed_split_datasets.py
python3 audit_condensed_split_datasets.py
```

The audit verifies valid regexes, compact unique readable names, exact source-row coverage, condensed metadata alignment, `covered_rows`, exact `num_rows_total` sums when all covered source rows have public counts, integer estimated totals when covered source rows have non-public split counts, and generated summaries for download status, local paths, and token estimates.
