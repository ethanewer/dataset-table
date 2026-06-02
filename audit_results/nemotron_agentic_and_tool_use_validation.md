# Nemotron Agentic and Tool-Use Collection Validation Notes

Validated on 2026-06-02 against the Hugging Face collection API for:

- `nvidia/nemotron-agentic-and-tool-use`

## Coverage

- The collection contains 9 dataset repos.
- 6 repos were already present in `datasets.csv`.
- Added the 3 missing repos:
  - `nvidia/Nemotron-RL-agent-calendar_scheduling`
  - `nvidia/Nemotron-RL-agent-workplace_assistant`
  - `nvidia/Nemotron-Terminal-Synthetic-Tasks`

## Row Counts

- `nvidia/Nemotron-RL-agent-calendar_scheduling`: exact dataset-server total, 4,000 rows.
- `nvidia/Nemotron-RL-agent-workplace_assistant`: exact dataset-server total, 1,800 rows.
- `nvidia/Nemotron-Terminal-Synthetic-Tasks`: dataset-server reports 0 rows because the repo releases tar archives rather than a tabular split. The card exposes only `100K<n<1M` as a size category, not an exact task count, so `num_rows=0` records the public dataset-server state. I did not expand the archives after the initial streaming attempt was stopped.

## Classification Decisions

- `nvidia/Nemotron-RL-agent-calendar_scheduling`
  - `is_rl=true` because it is a NeMo Gym RL dataset with verifier-ready `exp_cal_state`.
  - `is_agent=false` for consistency with the current schema: sampled rows are multi-turn scheduling prompts plus target calendar state, not tool, terminal, computer-use, or released agent trajectory traces.
  - `includes_verification=true` because rows include `exp_cal_state`.
- `nvidia/Nemotron-RL-agent-workplace_assistant`
  - `is_agent=true` because rows expose tool definitions, `ground_truth` tool actions, and `responses_api_agents` agent references.
  - `is_rl=true` because it is a NeMo Gym RL/tool-use task environment.
  - `includes_verification=true` because rows include `ground_truth` tool calls.
- `nvidia/Nemotron-Terminal-Synthetic-Tasks`
  - `is_code_swe_terminal=true` because the card describes Linux terminal tasks in Docker/tmux environments.
  - `is_agent=true` because the tasks are designed for autonomous terminal agents.
  - `is_rl=true` because the repo contains verifiable task environments with `tests/test.sh` verification suites.
  - `includes_verification=true` because each task directory is specified as including a pytest-based verification suite.

## Verification Columns

- `filtered_for_correctness=false` for all three new rows because none of the public metadata states that released rows/tasks are all successful agent completions.
- Non-RL/non-agent existing rows keep their prior metadata.
