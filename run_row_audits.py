#!/usr/bin/env python3
import argparse
import csv
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "current_datasets.csv"
SCHEMA_DOC = ROOT / "current_datasets_schema.md"
OUTPUT_SCHEMA = ROOT / "audit_row_schema.json"
OUT_DIR = ROOT / "audit_results"


def read_rows():
    with CSV_PATH.open(newline="") as f:
        return list(csv.DictReader(f))


def build_prompt(row, row_index):
    schema = SCHEMA_DOC.read_text()
    return f"""You are one worker in a row-by-row audit pipeline.

Audit exactly one row from current_datasets.csv. Do not edit files.

Your task:
1. Verify every cell in the row against primary sources where possible:
   - Hugging Face dataset card and dataset-server metadata.
   - Linked papers/repos only when needed.
   - Inspect 1-3 actual dataset samples when possible, especially for `reasoning`, `includes_verification`, and `filtered_for_correctness`.
2. For each CSV column, mark the cell as correct, incorrect, or uncertain.
3. If a cell is incorrect, provide the exact corrected CSV cell value as `suggested_value`.
4. Give compact source evidence with URLs, dataset-server endpoints, row/sample observations, or quoted field names.
5. Return only JSON matching the provided schema.

Important conventions from current_datasets_schema.md:
{schema}

Row index: {row_index}
Row JSON:
{json.dumps(row, ensure_ascii=False, indent=2)}

Be strict:
- Do not treat a data-generation framework as `agent_harness`.
- Do not treat underlying task tests/verifiers as `includes_verification=true` unless the released dataset rows include trajectory-level correctness/pass-fail/reward/target/verifier output.
- `filtered_for_correctness=true` only if released trajectories are all verified successful/reward=1.
- For `reasoning`, inspect samples where possible and align list values with `teacher_model` when teacher_model is a JSON list.
"""


def run_one(row, row_index, timeout):
    OUT_DIR.mkdir(exist_ok=True)
    dataset_safe = row["dataset_name"].replace("/", "__").replace(":", "_")
    output_file = OUT_DIR / f"{row_index:02d}_{dataset_safe}.json"
    prompt_file = OUT_DIR / f"{row_index:02d}_{dataset_safe}.prompt.txt"
    log_file = OUT_DIR / f"{row_index:02d}_{dataset_safe}.events.jsonl"
    prompt = build_prompt(row, row_index)
    prompt_file.write_text(prompt)

    cmd = [
        "codex",
        "exec",
        "--cd",
        str(ROOT),
        "--skip-git-repo-check",
        "--sandbox",
        "danger-full-access",
        "--output-schema",
        str(OUTPUT_SCHEMA),
        "--output-last-message",
        str(output_file),
        "--json",
        "-",
    ]
    env = os.environ.copy()
    env.setdefault("NO_COLOR", "1")
    with prompt_file.open("rb") as stdin, log_file.open("wb") as stdout:
        proc = subprocess.run(
            cmd,
            stdin=stdin,
            stdout=stdout,
            stderr=subprocess.STDOUT,
            cwd=ROOT,
            env=env,
            timeout=timeout,
        )
    return {
        "row_index": row_index,
        "dataset_name": row["dataset_name"],
        "returncode": proc.returncode,
        "output_file": str(output_file),
        "log_file": str(log_file),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--only", type=int, nargs="*", help="1-based row indexes to run")
    args = parser.parse_args()

    rows = read_rows()
    indexed = list(enumerate(rows, start=1))
    if args.only:
        only = set(args.only)
        indexed = [(i, r) for i, r in indexed if i in only]

    OUT_DIR.mkdir(exist_ok=True)
    manifest = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futures = [ex.submit(run_one, row, i, args.timeout) for i, row in indexed]
        for fut in as_completed(futures):
            result = fut.result()
            manifest.append(result)
            print(json.dumps(result), flush=True)

    manifest.sort(key=lambda x: x["row_index"])
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    failed = [m for m in manifest if m["returncode"] != 0]
    if failed:
        print("Some audits failed:", json.dumps(failed, indent=2), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
