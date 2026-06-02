# Open Coding Agents Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection APIs for:

- `allenai/open-coding-agents`
- nested collection item `allenai/open-coding-agents-specialization`

## Coverage

- Added all 7 direct dataset repos in `allenai/open-coding-agents`.
- Added all 6 dataset repos in the nested specialization collection because it is an item in the main Open Coding Agents collection.
- Excluded model repos from the collection.

## Row Counts

- Most Sera datasets have `viewer-partial` Hugging Face dataset-server metadata, so collection/viewer row counts can be lower than the dataset card's stated full trajectory count.
- `num_rows` uses each dataset card's stated trajectory count when it is higher or more complete than partial viewer metadata.

## Classification Decisions

- Sera rows are code/SWE agent trajectory datasets: `is_code_swe_terminal=true`, `is_agent=true`, `is_rl=false`.
- Dataset cards identify SVG rollouts on SWE-smith or specialization codebases, so `agent_harness=SVG`.
- Teacher models are `GLM-4.6` for Sera 4.6 rows and `GLM-4.5-Air` for Sera 4.5A rows.
- Samples expose explicit `<think>`/`thought` content in the trajectory messages, so `reasoning=true`.
- T1 rows have no verification, so `includes_verification=false`; T2 and best-subset rows include target/patch verification metadata, so `includes_verification=true`.
- `filtered_for_correctness=false` for all rows because card text does not claim the released trajectories are all verified successful completions.
