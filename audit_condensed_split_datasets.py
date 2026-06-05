#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

import generate_condensed_split_datasets as gen


ROOT = Path(__file__).resolve().parent
SOURCE_CSV = ROOT / "split_datasets.csv"
CONDENSED_CSV = ROOT / "condensed_split_datasets.csv"
AUDIT_OUT = ROOT / "audit_results" / "condensed_split_datasets_audit.json"


def read_rows(path):
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def compile_regex(pattern, errors, row_index, column):
    try:
        return re.compile(pattern)
    except re.error as exc:
        errors.append(f"condensed row {row_index}: {column} invalid regex: {exc}")
        return re.compile(r"a^")


def fullmatch(regex, value):
    return bool(regex.fullmatch(value))


def row_key(row):
    return f"{row['dataset_name']}::{row['hf_split']}"


def validate_local_path(value, errors, row_index):
    if not value:
        return
    if value.startswith("["):
        try:
            paths = json.loads(value)
        except json.JSONDecodeError as exc:
            errors.append(f"condensed row {row_index}: local_path invalid JSON list: {exc}")
            return
        if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
            errors.append(f"condensed row {row_index}: local_path JSON value must be a string array")
            return
    else:
        paths = [value]

    for path in paths:
        if not path.startswith("/wbl-fast/"):
            errors.append(f"condensed row {row_index}: local_path must be blank or under /wbl-fast")


def audit():
    errors = []
    warnings = []
    source_fields, source_rows = read_rows(SOURCE_CSV)
    condensed_fields, condensed_rows = read_rows(CONDENSED_CSV)

    if condensed_fields != gen.OUTPUT_COLUMNS:
        errors.append("condensed_split_datasets.csv header does not match condensed schema")

    compiled = []
    readable_names = set()
    for idx, row in enumerate(condensed_rows, start=1):
        if not row["readable_name"].strip():
            errors.append(f"condensed row {idx}: readable_name is required")
        if len(row["readable_name"]) > gen.MAX_READABLE_NAME_CHARS:
            errors.append(
                f"condensed row {idx}: readable_name exceeds "
                f"{gen.MAX_READABLE_NAME_CHARS} chars: {row['readable_name']}"
            )
        if row["readable_name"] in readable_names:
            errors.append(f"condensed row {idx}: duplicate readable_name {row['readable_name']}")
        readable_names.add(row["readable_name"])
        compiled.append(
            (
                idx,
                row,
                compile_regex(row["dataset_name_regex"], errors, idx, "dataset_name_regex"),
                compile_regex(row["hf_split_regex"], errors, idx, "hf_split_regex"),
                compile_regex(row["dataset_config_regex"], errors, idx, "dataset_config_regex"),
            )
        )
        try:
            int(row["covered_rows"])
        except ValueError:
            errors.append(f"condensed row {idx}: covered_rows must be an integer")
        if row["num_rows_total"]:
            try:
                int(row["num_rows_total"])
            except ValueError:
                errors.append(f"condensed row {idx}: num_rows_total must be blank or an integer")
        if row["downloaded"] not in {"true", "false"}:
            errors.append(f"condensed row {idx}: downloaded must be true or false")
        validate_local_path(row["local_path"], errors, idx)
        for column in [
            "qwen_estimated_tokens",
            "nemotron_estimated_tokens",
            "avg_estimated_tokens",
            "token_estimate_sample_rows",
        ]:
            if row[column]:
                try:
                    if int(row[column]) < 0:
                        errors.append(f"condensed row {idx}: {column} must be non-negative")
                except ValueError:
                    errors.append(f"condensed row {idx}: {column} must be blank or an integer")

    unused_estimated_total_names = sorted(set(gen.ESTIMATED_NUM_ROWS_TOTAL) - readable_names)
    if unused_estimated_total_names:
        errors.append(
            "estimated total names do not match condensed rows: "
            + ", ".join(unused_estimated_total_names)
        )

    matched_counts = {idx: 0 for idx, *_ in compiled}
    matched_num_rows = {idx: 0 for idx, *_ in compiled}
    matched_missing_num_rows = {idx: 0 for idx, *_ in compiled}
    matched_rows = {idx: [] for idx, *_ in compiled}
    source_seen = set()

    for source in source_rows:
        key = (source["dataset_name"], source["hf_split"])
        if key in source_seen:
            errors.append(f"duplicate source row key: {row_key(source)}")
        source_seen.add(key)

        matches = []
        for idx, condensed, name_re, split_re, config_re in compiled:
            if not fullmatch(name_re, source["dataset_name"]):
                continue
            if not fullmatch(split_re, source["hf_split"]):
                continue
            if not fullmatch(config_re, source["dataset_config"]):
                continue
            metadata_matches = all(source[column] == condensed[column] for column in gen.METADATA_COLUMNS)
            if metadata_matches and source["num_rows_source"] == condensed["num_rows_source"]:
                matches.append((idx, condensed))

        if len(matches) != 1:
            errors.append(f"{row_key(source)}: expected exactly one condensed match, found {len(matches)}")
            continue

        idx, _condensed = matches[0]
        matched_counts[idx] += 1
        matched_rows[idx].append(source)
        if source["num_rows"]:
            matched_num_rows[idx] += int(source["num_rows"])
        else:
            matched_missing_num_rows[idx] += 1

    for idx, condensed, *_ in compiled:
        expected_count = int(condensed["covered_rows"])
        if matched_counts[idx] != expected_count:
            errors.append(
                f"condensed row {idx}: covered_rows={expected_count}, matched {matched_counts[idx]}"
            )
        if condensed["num_rows_total"] and matched_missing_num_rows[idx] == 0:
            expected_total = int(condensed["num_rows_total"])
            if matched_num_rows[idx] != expected_total:
                errors.append(
                    f"condensed row {idx}: num_rows_total={expected_total}, "
                    f"matched total {matched_num_rows[idx]}"
                )
        expected_summary = gen.summary_values(matched_rows[idx])
        for column, expected_value in expected_summary.items():
            if condensed[column] != expected_value:
                errors.append(
                    f"condensed row {idx}: {column}={condensed[column]!r}, "
                    f"expected {expected_value!r}"
                )

    report = {
        "source_rows": len(source_rows),
        "condensed_rows": len(condensed_rows),
        "errors": errors,
        "warnings": warnings,
    }
    AUDIT_OUT.parent.mkdir(exist_ok=True)
    AUDIT_OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    report = audit()
    if report["errors"]:
        print(
            f"audit failed: {len(report['errors'])} errors; "
            f"report written to {AUDIT_OUT}"
        )
        for error in report["errors"][:40]:
            print(error)
        return 1
    print(
        f"audit ok: {report['source_rows']} source rows condensed to "
        f"{report['condensed_rows']} rows; report written to {AUDIT_OUT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
