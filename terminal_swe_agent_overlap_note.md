# Terminal/SWE Agent Dataset Overlap Note

This note distinguishes two overlap types for agent datasets in
`split_datasets.csv` where `is_code_swe_terminal=true` and `is_agent=true`.

- **Task overlap** means the user prompt and environment/task are the same, even
  if the rollout, harness, teacher, or tool calls differ.
- **Trajectory overlap** means the dataset row is the same trajectory: same
  task, same harness/teacher, and matching tool calls. A reused task with a
  different rollout is **not** trajectory overlap.

## Scope

Primary scope is the terminal/SWE agent rows in `split_datasets.csv`:

- `nvidia/Nemotron-SFT-OpenCode-v1` splits
- `nvidia/Nemotron-Terminal-Corpus` splits
- `nvidia/Nemotron-SFT-SWE-v2/openhands_swe`
- AllenAI SERA/SVG datasets
- `Sellopale/OpenThoughts-Agent-v1-SFT`
- `lambda/hermes-agent-reasoning-traces`
- `TeichAI/DeepSeek-v4-Pro-Agent`
- `open-thoughts/AgentTrove`
- `nebius/SWE-agent-trajectories`
- `AlienKevin/SWE-ZERO-12M-trajectories`
- `nvidia/Nemotron-SWE-v1/r2e_gym`
- `nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1`
- `nvidia/Nemotron-RL-Super-Training-Blends/swe1,swe2`
- `nvidia/Nemotron-Cascade-2-SFT-Data/swe`
- `nvidia/Nemotron-Cascade-2-SFT-Data/terminal_agent`
- `nvidia/SWE-Zero-openhands-trajectories`
- `nvidia/SWE-Hero-openhands-trajectories`
- `nvidia/Nemotron-Terminal-Synthetic-Tasks`

Parquet datasets could not be row-decoded in this environment because
`pyarrow`, `pandas`, `fastparquet`, `datasets`, and `duckdb` were unavailable.
Those datasets are classified from dataset cards, filenames, CSV metadata, and
local JSONL source fields where available.

## Matrix Key

- `ID:n` - exact stable local task identifier overlap of `n` unique IDs.
- `ID:set` - full stable ID-set overlap, but not necessarily one unique ID per row.
- `SRC` - declared shared source corpora; task overlap is likely but not row-counted.
- `SRC?` - weak or partial source-family overlap.
- `SUBSET` - dataset card declares a subset/superset relation.
- `P-TRJ` - potential trajectory overlap/repackaging, exact row equality not proven.
- `0-ROW` - exact canonical row equality checked and found zero row overlap.
- blank - no evidence of overlap found in this pass.

## Task Overlap Matrix

Rows/columns are dataset families, not every split, to keep the matrix readable.
Internal split overlap is summarized in the diagonal and detailed below.

| Task overlap | OC | SERA | NTC | C2T | SFT2 | SWEv1 | RLP | RLS | C2S | SWZ | SWH | SZ12 | AT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OC | ID:17k/25k |  |  |  |  |  |  |  |  |  |  |  |  |
| SERA |  | ID:many |  |  |  |  |  |  |  |  |  |  | SRC |
| NTC |  |  |  | SRC |  |  |  |  |  |  |  |  |  |
| C2T |  |  | SRC |  |  |  |  |  |  |  |  |  |  |
| SFT2 |  |  |  |  |  | SRC | SRC | SRC | SRC? | SRC | SRC |  | SRC |
| SWEv1 |  |  |  |  | SRC |  | SRC | SRC | SRC | SRC | SRC |  | SRC |
| RLP |  |  |  |  | SRC | SRC |  | ID:set | SRC | SRC | SRC |  | SRC |
| RLS |  |  |  |  | SRC | SRC | ID:set |  | SRC | SRC | SRC |  | SRC |
| C2S |  |  |  |  | SRC? | SRC | SRC | SRC |  | SRC | SRC |  | SRC |
| SWZ |  |  |  |  | SRC | SRC | SRC | SRC | SRC |  | SRC | SRC? | SRC |
| SWH |  |  |  |  | SRC | SRC | SRC | SRC | SRC | SRC |  |  | SRC |
| SZ12 |  |  |  |  |  |  |  |  |  | SRC? |  |  |  |
| AT |  | SRC |  |  | SRC | SRC | SRC | SRC | SRC | SRC | SRC |  |  |

Aliases:

- `OC`: `nvidia/Nemotron-SFT-OpenCode-v1`
- `SERA`: all AllenAI SERA/SVG rows
- `NTC`: `nvidia/Nemotron-Terminal-Corpus`
- `C2T`: `nvidia/Nemotron-Cascade-2-SFT-Data/terminal_agent`
- `SFT2`: `nvidia/Nemotron-SFT-SWE-v2/openhands_swe`
- `SWEv1`: `nvidia/Nemotron-SWE-v1/r2e_gym`
- `RLP`: `nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1`
- `RLS`: `nvidia/Nemotron-RL-Super-Training-Blends/swe1,swe2`
- `C2S`: `nvidia/Nemotron-Cascade-2-SFT-Data/swe` agentic portion
- `SWZ`: `nvidia/SWE-Zero-openhands-trajectories`
- `SWH`: `nvidia/SWE-Hero-openhands-trajectories`
- `SZ12`: `AlienKevin/SWE-ZERO-12M-trajectories`
- `AT`: `open-thoughts/AgentTrove`

Datasets with no overlap evidence from this pass:

- `Sellopale/OpenThoughts-Agent-v1-SFT`
- `lambda/hermes-agent-reasoning-traces`
- `TeichAI/DeepSeek-v4-Pro-Agent`
- `nebius/SWE-agent-trajectories`
- `nvidia/Nemotron-Terminal-Synthetic-Tasks` (0 rows in table)

## Trajectory Overlap Matrix

This matrix is intentionally much sparser. Most shared source/task families use
different harnesses, teachers, or rollouts, so they are task overlap but not
trajectory overlap.

| Trajectory overlap | OC | SERA | NTC | C2T | SFT2 | SWEv1 | RLP | RLS | C2S | SWZ | SWH | SZ12 | AT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OC | task-only |  |  |  |  |  |  |  |  |  |  |  |  |
| SERA |  | P-TRJ |  |  |  |  |  |  |  |  |  |  |  |
| NTC |  |  |  | P-TRJ |  |  |  |  |  |  |  |  |  |
| C2T |  |  | P-TRJ |  |  |  |  |  |  |  |  |  |  |
| SFT2 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| SWEv1 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| RLP |  |  |  |  |  |  |  | 0-ROW |  |  |  |  |  |
| RLS |  |  |  |  |  |  | 0-ROW |  |  |  |  |  |  |
| C2S |  |  |  |  |  |  |  |  |  |  |  |  |  |
| SWZ |  |  |  |  |  |  |  |  |  |  | task-only | task-only |  |
| SWH |  |  |  |  |  |  |  |  |  | task-only |  |  |  |
| SZ12 |  |  |  |  |  |  |  |  |  | task-only |  |  |  |
| AT |  |  |  |  |  |  |  |  |  |  |  |  |  |

Notes on trajectory matrix:

- `RLP` vs `RLS/swe1`: the two files have the same 50,661 row count, the
  same 3,219 `trajectory_id` set, and the same 2,484 `metadata.instance_id`
  set. However canonical JSON row comparison found `0/50,661` identical rows.
  This is task overlap, not row-exact trajectory overlap.
- `C2T` vs `NTC`: Cascade 2 terminal rows sampled `1000/1000` with
  `source=Nemotron-Terminal-Corpus`, and the Cascade 2 README says terminal
  samples are sourced from Nemotron Terminal Corpus. Exact row/trajectory
  equality is unproven because the source Terminal Corpus local files are
  parquet and no parquet reader is installed here.
- `SERA`: some datasets are explicitly subsets/supersets or first/second
  rollout variants. T1/T2 pairs share task IDs but are different rollouts.
  `SERA-4.6-Lite-Best-Subset` is declared to contain samples from
  `Sera-4.6-Lite-T1` and `Sera-4.6-Lite-T2`, so trajectory overlap is
  plausible, but row-exact equality was not proven.
- `OC`: exact UUID overlaps exist across split variants, but sampled common
  UUID rows have different message counts and categories. Treat as task overlap
  only unless a stricter row-hash pass proves otherwise.

## Exact Task-ID Evidence

### OpenCode Internal Splits

Stable `uuid` overlap:

| Pair | Shared UUIDs | Classification |
|---|---:|---|
| `agent_skills` vs `agent_skills_question_tool` | 17,261 | task overlap |
| `general` vs `question_tool` | 25,700 | task overlap |

Sampled shared UUIDs had different message counts:

- `agent_skills` sample: 7 messages; `agent_skills_question_tool`: 15 messages.
- `general` sample: 21 messages; `question_tool`: 33 messages.

That indicates reused tasks with different trajectories/tool interactions.

### SERA/SVG Internal Splits

Stable `instance_id` overlap:

| Pair | Shared `instance_id`s |
|---|---:|
| `Sera-4.5A-Django-T1` vs `Sera-4.5A-Django-T2` | 21,900 |
| `Sera-4.5A-Sphinx-T1` vs `Sera-4.5A-Sphinx-T2` | 12,676 |
| `Sera-4.5A-Sympy-T1` vs `Sera-4.5A-Sympy-T2` | 25,397 |
| `Sera-4.5A-Full-T1` vs `Sera-4.5A-Lite-T1` | 36,607 |
| `Sera-4.5A-Full-T2` vs `Sera-4.5A-Lite-T2` | 35,615 |
| `Sera-4.5A-Full-T1` vs `Sera-4.5A-Full-T2` | 65,463 |
| `Sera-4.5A-Lite-T1` vs `Sera-4.5A-Lite-T2` | 32,852 |
| `Sera-4.6-Lite-T1` vs `Sera-4.6-Lite-T2` | 36,083 |
| `SERA-4.6-Lite-Best-Subset` vs `Sera-4.6-Lite-T1` | 29,687 |
| `SERA-4.6-Lite-Best-Subset` vs `Sera-4.6-Lite-T2` | 29,561 |

Additional cross-version SERA overlaps exist between 4.5A and 4.6 Lite/Best
files, ranging from 6,140 to 15,233 shared `instance_id`s.

## Source-Lineage Evidence

### Cascade 2

- `nvidia/Nemotron-Cascade-2-SFT-Data/terminal_agent`: local sample shows
  `1000/1000` rows with `source=Nemotron-Terminal-Corpus`; README says terminal
  agent samples are sourced from `nvidia/Nemotron-Terminal-Corpus`.
- `nvidia/Nemotron-Cascade-2-SFT-Data/swe`: local sample shows
  `source=nebius/SWE-rebench` for the agentic file and
  `source=Nemotron-Cascade-SFT-SWE` for the agentless file. README says agentic
  SWE samples are drawn from SWE-Gym, SWE-rebench, and R2E-Gym-Subset.

### NVIDIA OpenHands SWE Family

Potential task overlap, not proven trajectory overlap:

- `nvidia/Nemotron-SFT-SWE-v2/openhands_swe`: card says OpenHands trajectories
  from SWE-Gym and R2E-Gym-Subset prompts.
- `nvidia/Nemotron-SWE-v1/r2e_gym`: local rows include
  `R2E-Gym/R2E-Gym-Subset` and `SWE-Gym/SWE-Gym`.
- `nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1`: card says refactored SWE-Gym,
  R2E-Gym, and SWE-Bench-Verified for OpenHands/NeMo Gym.
- `nvidia/Nemotron-RL-Super-Training-Blends/swe1,swe2`: card says SWE 1/2 are
  blends of R2E-Gym-Subset and SWE-Gym.
- `nvidia/SWE-Zero-openhands-trajectories` and
  `nvidia/SWE-Hero-openhands-trajectories`: cards list overlapping source
  families including SWE-Gym, R2E-Gym-Subset, and SWE-rebench.

### AgentTrove

`open-thoughts/AgentTrove` is a broad concatenated corpus. Its card lists source
families including `r2egym`, `SWEGym`, and `swesmith`, so task overlap is
potential with NVIDIA/AllenAI datasets that use those same task families. The
harness/teacher mix differs, so this is not trajectory overlap evidence.

### SWE-ZERO 12M

`AlienKevin/SWE-ZERO-12M-trajectories` is a 10x scale-up using the SWE-ZERO
execution-free recipe and starts from `nebius/SWE-rebench-V2-PRs`. This is
potential task overlap with SWE-Zero-style data, but its harness
(`mini-swe-agent v1`) and teacher differ from the NVIDIA OpenHands SWE-Zero
dataset, so it is not trajectory overlap evidence.

## Practical Dedupe Guidance

For SFT training blend construction:

1. Deduplicate **tasks** first using stable IDs when available:
   `uuid`, `instance_id`, `trajectory_id`, repo/commit IDs, and source task IDs.
2. Treat the following as high-risk task-overlap families:
   OpenCode internal splits, SERA internal splits, NVIDIA OpenHands SWE family,
   Cascade 2 terminal vs Terminal Corpus, RL Pivot vs RL Super SWE, and
   AgentTrove vs R2E/SWEGym/SWESmith-derived datasets.
3. Only deduplicate **trajectories** when canonical row or canonical tool-call
   hashes match. Shared task IDs alone are not enough.
4. For parquet-only datasets, install a parquet reader and compute:
   task key hashes from prompt/environment IDs, and trajectory hashes from
   normalized messages/tool calls plus harness and teacher metadata.
