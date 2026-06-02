#!/usr/bin/env python3
import argparse
import csv
import json
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import generate_split_datasets as gen


ROOT = Path(__file__).resolve().parent
SPLIT_CSV = ROOT / "split_datasets.csv"
AUDIT_OUT = ROOT / "audit_results" / "split_datasets_audit.json"

BOOL_COLUMNS = [
    "is_code_swe_terminal",
    "is_agent",
    "is_rl",
    "is_pretraining",
    "already_included",
]

JSON_OR_BOOL_COLUMNS = ["reasoning"]
JSON_COLUMNS = ["aux_models"]
ALLOWED_NUM_ROW_SOURCES = {
    "dataset_server_exact",
    "dataset_server_partial",
    "dataset_server_estimated",
    "dataset_card_exact",
    "parent_single_split",
    "not_public_per_split",
}


def read_csv(path):
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def parse_json_cell(row, column, errors):
    value = row[column]
    if not value or value[0] not in "[{":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        errors.append(f"{row_key(row)}: {column} invalid JSON: {exc}")
        return None


def row_key(row):
    return f"{row['dataset_name']}::{row['dataset_config']}::{row['split']}"


def truth(value):
    return str(value).lower() == "true"


def expected_split_url(name, config, split):
    return (
        f"https://huggingface.co/datasets/{name}"
        f"?config={urllib.parse.quote(config, safe='')}"
        f"&split={urllib.parse.quote(split, safe='')}"
    )


def fetch_all_metadata(parent_rows, max_workers):
    metas = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(gen.fetch_metadata, row): row["dataset_name"] for row in parent_rows}
        for future in as_completed(futures):
            meta = future.result()
            metas[meta["row"]["dataset_name"]] = meta
    return metas


def infer_parent_rows(split_rows, errors):
    parent_by_name = {}
    for row in split_rows:
        name = row["dataset_name"]
        parent_rows = row["parent_num_rows"]
        if name not in parent_by_name:
            parent_by_name[name] = {"dataset_name": name, "num_rows": parent_rows}
        elif parent_by_name[name]["num_rows"] != parent_rows:
            errors.append(
                f"{name}: inconsistent parent_num_rows values "
                f"{parent_by_name[name]['num_rows']} and {parent_rows}"
            )
    return list(parent_by_name.values()), parent_by_name


def audit_schema(rows, fieldnames, parent_by_name, errors):
    if fieldnames != gen.OUTPUT_COLUMNS:
        errors.append("split_datasets.csv header does not match split schema")

    seen = set()
    for row in rows:
        key = (row["dataset_name"], row["dataset_config"], row["split"])
        if key in seen:
            errors.append(f"duplicate split row: {row_key(row)}")
        seen.add(key)

        parent = parent_by_name.get(row["dataset_name"])
        if not parent:
            errors.append(f"{row_key(row)}: dataset_name could not be inferred from split CSV")
            continue

        expected_dataset_url = f"https://huggingface.co/datasets/{row['dataset_name']}"
        if row["dataset_url"] != expected_dataset_url:
            errors.append(f"{row_key(row)}: dataset_url should be {expected_dataset_url}")
        expected_url = expected_split_url(row["dataset_name"], row["dataset_config"], row["split"])
        if row["split_url"] != expected_url:
            errors.append(f"{row_key(row)}: split_url should be {expected_url}")
        if row["parent_num_rows"] != parent["num_rows"]:
            errors.append(f"{row_key(row)}: parent_num_rows should be {parent['num_rows']}")

        for column in BOOL_COLUMNS:
            if row[column] not in {"true", "false"}:
                errors.append(f"{row_key(row)}: {column} must be true or false")
        for column in ["filtered_for_correctness", "includes_verification"]:
            if row[column] not in {"", "true", "false"}:
                errors.append(f"{row_key(row)}: {column} must be blank, true, or false")
        if row["num_rows"]:
            try:
                if int(row["num_rows"]) < 0:
                    errors.append(f"{row_key(row)}: num_rows must be non-negative")
            except ValueError:
                errors.append(f"{row_key(row)}: num_rows must be blank or an integer")
        if not row["num_rows_source"]:
            errors.append(f"{row_key(row)}: num_rows_source is required")
        elif row["num_rows_source"] not in ALLOWED_NUM_ROW_SOURCES:
            errors.append(f"{row_key(row)}: unknown num_rows_source {row['num_rows_source']}")

        teacher = parse_json_cell(row, "teacher_model", errors)
        reasoning = parse_json_cell(row, "reasoning", errors)
        aux = parse_json_cell(row, "aux_models", errors)
        if row["reasoning"] not in {"true", "false"} and reasoning is None:
            errors.append(f"{row_key(row)}: reasoning must be true, false, or a JSON list")
        if isinstance(teacher, list):
            if not isinstance(reasoning, list):
                # Split-level reasoning_on/off intentionally collapses this to a scalar.
                if row["split"] not in {"reasoning_on", "reasoning_off"}:
                    errors.append(f"{row_key(row)}: JSON-list teacher_model requires JSON-list reasoning")
            elif len(teacher) != len(reasoning):
                errors.append(f"{row_key(row)}: teacher_model and reasoning list lengths differ")
        if aux is not None:
            if not isinstance(aux, list):
                errors.append(f"{row_key(row)}: aux_models must be a JSON array")
            elif not all(isinstance(item, dict) and "model" in item and "use" in item for item in aux):
                errors.append(f"{row_key(row)}: aux_models entries must contain model and use")

        if not truth(row["is_agent"]) and row["agent_harness"]:
            errors.append(f"{row_key(row)}: non-agent rows must have blank agent_harness")
        if not truth(row["is_agent"]) and not truth(row["is_rl"]):
            if row["filtered_for_correctness"] or row["includes_verification"]:
                errors.append(f"{row_key(row)}: non-agent/non-RL rows should have blank verification columns")
        if truth(row["is_agent"]) or truth(row["is_rl"]):
            if row["filtered_for_correctness"] == "":
                errors.append(f"{row_key(row)}: agent/RL rows require filtered_for_correctness")
            if row["includes_verification"] == "":
                errors.append(f"{row_key(row)}: agent/RL rows require includes_verification")


def audit_split_coverage(rows, metas, errors):
    actual = {(row["dataset_name"], row["dataset_config"], row["split"]) for row in rows}
    expected = set()
    for name, meta in metas.items():
        for config, split in gen.discover_splits(meta):
            expected.add((name, config, split))

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append("missing split rows: " + ", ".join(f"{n}::{c}::{s}" for n, c, s in missing[:50]))
    if extra:
        errors.append("extra split rows: " + ", ".join(f"{n}::{c}::{s}" for n, c, s in extra[:50]))


def audit_counts(rows, metas, errors, warnings):
    by_dataset = {}
    for row in rows:
        by_dataset.setdefault(row["dataset_name"], []).append(row)

    for name, group in by_dataset.items():
        meta = metas[name]
        for row in group:
            config = row["dataset_config"]
            split = row["split"]
            expected_count, expected_source = gen.row_count(meta, config, split)
            if row["num_rows"] != expected_count:
                errors.append(
                    f"{row_key(row)}: num_rows should be {expected_count!r} from {expected_source}, "
                    f"found {row['num_rows']!r}"
                )
            if row["num_rows_source"] != expected_source:
                errors.append(
                    f"{row_key(row)}: num_rows_source should be {expected_source}, "
                    f"found {row['num_rows_source']}"
                )

        if all(row["num_rows"] and row["num_rows_source"] in {"dataset_server_exact", "dataset_card_exact", "parent_single_split"} for row in group):
            total = sum(int(row["num_rows"]) for row in group)
            parent_total = int(group[0]["parent_num_rows"])
            if total != parent_total:
                errors.append(f"{name}: exact split num_rows sum {total} != parent_num_rows {parent_total}")
        elif any(row["num_rows_source"] == "not_public_per_split" for row in group):
            warnings.append(f"{name}: one or more split counts are not public per split")
        elif any(row["num_rows_source"] == "dataset_server_partial" for row in group):
            warnings.append(f"{name}: one or more split counts come from a partial dataset-server view")


def audit_split_classification(rows, errors):
    by_key = {(row["dataset_name"], row["dataset_config"], row["split"]): row for row in rows}

    def require(key, column, expected):
        row = by_key.get(key)
        if not row:
            errors.append(f"missing classification check target: {key}")
            return
        if row[column] != expected:
            errors.append(f"{row_key(row)}: expected {column}={expected}, found {row[column]}")

    require(("nvidia/Nemotron-SFT-SWE-v2", "default", "agentless"), "is_agent", "false")
    require(("nvidia/Nemotron-SFT-SWE-v2", "default", "agentless"), "agent_harness", "")
    require(("nvidia/Nemotron-SFT-SWE-v2", "default", "openhands_swe"), "is_agent", "true")
    require(("nvidia/Nemotron-SFT-SWE-v2", "default", "openhands_swe"), "agent_harness", "OpenHands")
    require(("nvidia/Nemotron-SFT-Instruction-Following-Chat-v2", "default", "reasoning_off"), "reasoning", "false")
    require(("nvidia/Nemotron-SFT-Instruction-Following-Chat-v2", "default", "reasoning_on"), "reasoning", "true")

    for key in gen.AGENT_FALSE_SPLITS:
        require(key, "is_agent", "false")
        require(key, "agent_harness", "")
    for key in gen.AGENT_TRUE_SPLITS:
        require(key, "is_agent", "true")

    for row in rows:
        label = gen.split_label(row["dataset_name"], row["dataset_config"], row["split"])
        if any(token in label for token in ["code", "swe", "terminal", "competitive", "python", "cpp", "sql", "exercism", "bash"]):
            if not any(token in label for token in ["cc_math", "math_code"]):
                if row["is_code_swe_terminal"] != "true":
                    errors.append(f"{row_key(row)}: code/SWE/terminal-looking split should be is_code_swe_terminal=true")
        if "algorithmic" in label and row["is_code_swe_terminal"] != "false":
            errors.append(f"{row_key(row)}: algorithmic pretraining split should not be classified as code/SWE/terminal")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-workers", type=int, default=8)
    parser.add_argument("--csv", type=Path, default=SPLIT_CSV)
    parser.add_argument("--output", type=Path, default=AUDIT_OUT)
    args = parser.parse_args()

    errors = []
    warnings = []
    fieldnames, rows = read_csv(args.csv)
    parent_rows, parent_by_name = infer_parent_rows(rows, errors)

    audit_schema(rows, fieldnames, parent_by_name, errors)
    metas = fetch_all_metadata(parent_rows, args.max_workers)
    audit_split_coverage(rows, metas, errors)
    audit_counts(rows, metas, errors, warnings)
    audit_split_classification(rows, errors)

    report = {
        "csv": str(args.csv),
        "rows": len(rows),
        "datasets": len({row["dataset_name"] for row in rows}),
        "errors": errors,
        "warnings": warnings,
    }
    args.output.parent.mkdir(exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2))

    if errors:
        print(f"audit failed: {len(errors)} errors; report written to {args.output}")
        for error in errors[:40]:
            print(error)
        return 1

    print(f"audit ok: {len(rows)} rows; {len(warnings)} warnings; report written to {args.output}")
    for warning in warnings[:20]:
        print("warning:", warning)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
