# OLMo 3 Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection APIs for:

- `allenai/olmo-3-post-training`
- `allenai/olmo-3-pre-training`

## Coverage

- Added all dataset repos directly listed in the two collections: 18 post-training datasets and 10 pre-training datasets.
- Excluded model repos from the same collections.
- Kept the existing `allenai/Dolci-Think-SFT-7B` row and added the remaining collection datasets as new rows.

## Row Counts

- Post-training counts come from collection `datasetsServerInfo.numRows` and matching dataset-server `/size` responses.
- Pre-training rows use dataset-server exact/estimated row counts where the viewer is partially materialized.
- For large pool or non-materialized pre-training repos, `num_rows` uses card-stated document totals when available.
- `allenai/dolma3_dolmino_mix-100B-1125` and `allenai/dolma3_longmino_mix-100B-1125` currently expose `0` rows through Hugging Face dataset-server/collection metadata and do not state document counts on the cards, so they are recorded as `0`.

## Classification Decisions

- RL datasets with `ground_truth`, verifier, reward, or rollout-count fields are marked `is_rl=true` and `includes_verification=true`.
- RL prompt/task datasets are not marked `is_agent=true`; they are not completed supervised agent trajectories.
- Tool-use SFT rows are treated as function-calling/chat SFT data, not agent trajectory datasets.
- Dolmino pre-training pools/mixes are marked `reasoning=true` because their cards include reasoning-trace configurations; broad Dolma and Longmino pre-training mixes are marked `reasoning=false`.
- Broad mixed datasets with no single documented response generator use `teacher_model=not_specified`; explicitly exposed `chosen_model`/`rejected_model` fields are recorded as teacher model lists.
