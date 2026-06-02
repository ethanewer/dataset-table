# Nemotron Pretraining Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection API for:

- `nvidia/nemotron-pre-training-datasets`

## Coverage

- Added all 10 dataset repos directly listed in the collection.
- Excluded no dataset repos; the collection items are all datasets.
- Several repos are gated, so dataset-server `/info` and `/size` are unavailable without authentication, but the collection API exposes viewer row counts and the dataset API exposes cards/configs.

## Row Counts

- `num_rows` uses collection `datasetsServerInfo.numRows` for all 10 rows.
- Public, ungated rows were cross-checked with dataset-server where available.

## Pretraining Classification

- Added `is_pretraining` as a boolean column.
- Marked the AllenAI OLMo 3 pre-training collection rows as `true`.
- Marked Nemotron raw/synthetic text, code, math, Common Crawl, and specialized pretraining rows as `true`.
- Marked `nvidia/Nemotron-Pretraining-SFT-v1` as `false` because its card and sample configs describe SFT-style code/math/general data, which is mainly LLM instruction/conversation-style data rather than next-token-prediction corpus data.
- Marked existing SFT, DPO, RL, safety, and agent trajectory rows as `false`.

## Code Classification

- `is_code_swe_terminal=true` is reserved for datasets that are primarily code, formal proof code, SWE, terminal, or agentic coding data.
- Kept code-specific corpora true: `Nemotron-CC-Code-v1`, `Nemotron-Pretraining-Code-v1`, and `Nemotron-Pretraining-Code-v2`.
- Kept `Nemotron-Pretraining-Specialized-v1.1` true because the public card shows the Code Concepts subset dominates the release by both tokens and rows.
- Set mixed/broad releases false: `Nemotron-Pretraining-Dataset-sample`, `Nemotron-Pretraining-Specialized-v1`, and `Nemotron-Pretraining-SFT-v1`.

## Other Metadata Decisions

- Gated rows that only expose collection/card metadata use `teacher_model=not_specified` unless the public card identifies generation models.
- `Nemotron-Pretraining-Specialized-v1` and `v1.1` use JSON teacher-model lists from their public cards, with `reasoning=true` because the named subsets include reasoning/STEM/formal-logic data.
- Agent/RL-only verification columns remain blank because these are not agent trajectory or RL datasets.
