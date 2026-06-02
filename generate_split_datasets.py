#!/usr/bin/env python3
import argparse
import csv
import json
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_CSV = ROOT / "datasets.csv"
OUTPUT_CSV = ROOT / "split_datasets.csv"

OUTPUT_COLUMNS = [
    "dataset_name",
    "dataset_config",
    "split",
    "dataset_url",
    "split_url",
    "is_code_swe_terminal",
    "is_agent",
    "is_rl",
    "is_pretraining",
    "reasoning",
    "filtered_for_correctness",
    "includes_verification",
    "teacher_model",
    "aux_models",
    "agent_harness",
    "num_rows",
    "num_rows_source",
    "parent_num_rows",
    "already_included",
]


def k(dataset, config, split):
    return (dataset, config, split)


# Exact split counts from dataset cards when dataset-server exposes split names
# but not per-split sizes.
KNOWN_SPLIT_COUNTS = {
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "code_de"): 133322,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "code_es"): 131578,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "code_fr"): 136045,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "code_it"): 143122,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "code_ja"): 126393,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "code_zh"): 154653,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "math_de"): 128846,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "math_es"): 102866,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "math_fr"): 115916,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "math_it"): 130388,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "math_ja"): 101820,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "math_zh"): 88594,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "stem_de"): 261205,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "stem_es"): 262353,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "stem_fr"): 264221,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "stem_it"): 269240,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "stem_ja"): 256624,
    k("nvidia/Nemotron-SFT-Multilingual-v1", "default", "stem_zh"): 258069,
    k("nvidia/Nemotron-Instruction-Following-Chat-v1", "default", "chat_if"): 426009,
    k("nvidia/Nemotron-Instruction-Following-Chat-v1", "default", "structured_outputs"): 4969,
    k("nvidia/Nemotron-SFT-Competitive-Programming-v2", "default", "competitive_coding_cpp"): 332559,
    k("nvidia/Nemotron-SFT-Competitive-Programming-v2", "default", "competitive_coding_python"): 336568,
    k("nvidia/Nemotron-SFT-Competitive-Programming-v2", "default", "exercism"): 79244,
    k("nvidia/Nemotron-SFT-Competitive-Programming-v2", "default", "text_to_sql"): 96564,
    k("nvidia/Nemotron-SFT-Agentic-v2", "default", "tool_calling"): 707052,
    k("nvidia/Nemotron-SFT-Agentic-v2", "default", "interactive_agent"): 278880,
    k("nvidia/Nemotron-SFT-Agentic-v2", "default", "search"): 5968,
    k("nvidia/Nemotron-SFT-SWE-v2", "default", "agentless"): 209976,
    k("nvidia/Nemotron-SFT-SWE-v2", "default", "openhands_swe"): 46278,
    k("nvidia/Nemotron-CrossThink", "default", "train_qa"): 187496,
    k("nvidia/Nemotron-CrossThink", "default", "train_math"): 99880,
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlvr1"): 138712,
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlvr2"): 156278,
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlvr3"): 107037,
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "swe1"): 50661,
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "swe2"): 1444,
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlhf"): 25171,
}

AGENT_TRUE_SPLITS = {
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "conversational_agent", "train"),
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "swe", "train"),
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "terminal_agent", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "tool_calling", "train"),
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "swe1"),
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "swe2"),
}

AGENT_FALSE_SPLITS = {
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "chat", "train"),
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "instruction_following", "train"),
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "math", "train"),
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "safety", "train"),
    k("nvidia/Nemotron-Cascade-2-SFT-Data", "science", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "code", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "general", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "instruction-following", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "math", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "science", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "swe_localization", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "swe_repair", "train"),
    k("nvidia/Nemotron-Cascade-SFT-Stage-2", "swe_testgen", "train"),
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlvr1"),
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlvr2"),
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlvr3"),
    k("nvidia/Nemotron-RL-Super-Training-Blends", "default", "rlhf"),
}


def curl_json(url, timeout=25):
    proc = subprocess.run(
        ["curl", "-fsSL", "--max-time", str(timeout), url],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return None, proc.stderr.strip()
    try:
        return json.loads(proc.stdout), ""
    except json.JSONDecodeError as exc:
        return None, str(exc)


def read_parent_rows():
    with INPUT_CSV.open(newline="") as f:
        return list(csv.DictReader(f))


def fetch_metadata(row):
    name = row["dataset_name"]
    encoded = urllib.parse.quote(name, safe="")
    splits, splits_error = curl_json(f"https://datasets-server.huggingface.co/splits?dataset={encoded}")
    size, size_error = curl_json(f"https://datasets-server.huggingface.co/size?dataset={encoded}")
    api, api_error = curl_json(f"https://huggingface.co/api/datasets/{name}")
    return {
        "row": row,
        "splits": splits,
        "splits_error": splits_error,
        "size": size,
        "size_error": size_error,
        "api": api,
        "api_error": api_error,
    }


def iter_api_split_keys(api):
    card = (api or {}).get("cardData") or {}
    for config in card.get("configs") or []:
        config_name = str(config.get("config_name") or "default")
        for data_file in config.get("data_files") or []:
            split = data_file.get("split")
            if split:
                yield config_name, str(split)

    info = card.get("dataset_info")
    infos = info if isinstance(info, list) else [info] if isinstance(info, dict) else []
    for entry in infos:
        config_name = str(entry.get("config_name") or entry.get("builder_name") or "default")
        for split in entry.get("splits") or []:
            name = split.get("name")
            if name:
                yield config_name, str(name)


def split_size_map(size):
    out = {}
    partial = bool((size or {}).get("partial"))
    for split in (((size or {}).get("size") or {}).get("splits") or []):
        config = str(split.get("config") or "default")
        split_name = str(split.get("split") or "train")
        value = split.get("num_rows")
        source = "dataset_server_partial" if partial else "dataset_server_exact"
        if value is None and split.get("estimated_num_rows") is not None:
            value = split.get("estimated_num_rows")
            source = "dataset_server_estimated"
        if value is not None:
            out[(config, split_name)] = (int(value), source)
    return out


def discover_splits(meta):
    row = meta["row"]
    name = row["dataset_name"]
    keys = []
    seen = set()

    for split in (meta["splits"] or {}).get("splits") or []:
        config = str(split.get("config") or "default")
        split_name = str(split.get("split") or "train")
        if (config, split_name) not in seen:
            seen.add((config, split_name))
            keys.append((config, split_name))

    for config, split_name in iter_api_split_keys(meta["api"]):
        if (config, split_name) not in seen:
            seen.add((config, split_name))
            keys.append((config, split_name))

    if not keys:
        keys.append(("default", "train"))
    return keys


def truth(value):
    return str(value).strip().lower() == "true"


def bool_cell(value):
    return "true" if value else "false"


def split_label(name, config, split):
    return f"{name} {config} {split}".lower().replace("-", "_")


def has_any(label, needles):
    return any(needle in label for needle in needles)


def override_code(parent, name, config, split):
    label = split_label(name, config, split)
    non_code_overrides = [
        "math", "science", "stem", "finance", "safety", "personas", "chat",
        "general", "instruction_following", "multilingual", "cc_math",
        "formal_logic", "economics", "multiple_choice", "rqa", "wiki_rewrite",
        "algorithmic",
    ]
    code_overrides = [
        "code", "swe", "terminal", "opencode", "competitive", "python", "cpp",
        "sql", "exercism", "bash", "programming", "scientific_coding",
        "code_concepts", "code_metadata", "synthetic_code",
    ]

    if has_any(label, code_overrides):
        return True
    if truth(parent["is_code_swe_terminal"]) and has_any(label, non_code_overrides):
        return False
    return truth(parent["is_code_swe_terminal"])


def override_agent(parent, name, config, split):
    split_key = k(name, config, split)
    if split_key in AGENT_TRUE_SPLITS:
        return True
    if split_key in AGENT_FALSE_SPLITS:
        return False

    label = split_label(name, config, split)
    if "agentless" in label:
        return False
    agent_overrides = [
        "openhands", "terminal_agent", "conversational_agent", "interactive_agent",
        "tool_calling", "function_calling", "question_tool", "agent_skills",
        "opencode", "bash_only_tool", "workplace_assistant",
    ]
    if has_any(label, agent_overrides):
        return True
    return truth(parent["is_agent"])


def override_harness(parent, is_agent, name, config, split):
    if not is_agent:
        return ""
    label = split_label(name, config, split)
    if "openhands" in label:
        return "OpenHands"
    if "opencode" in label or "bash_only_tool" in label or "agent_skills" in label or "question_tool" in label:
        return "OpenCode CLI"
    if "terminal" in label:
        return parent.get("agent_harness") or "Terminus-2"
    return parent.get("agent_harness") or ""


def override_reasoning(parent, name, config, split):
    label = split_label(name, config, split)
    if "reasoning_off" in label:
        return "false"
    if "reasoning_on" in label:
        return "true"
    return parent["reasoning"]


def row_count(meta, config, split):
    parent = meta["row"]
    name = parent["dataset_name"]
    parent_rows = int(parent["num_rows"])
    key = (name, config, split)
    size_counts = split_size_map(meta["size"])

    if (config, split) in size_counts:
        count, source = size_counts[(config, split)]
        # Partial materialization can undercount relative to audited card totals.
        if source == "dataset_server_partial" and key in KNOWN_SPLIT_COUNTS:
            return str(KNOWN_SPLIT_COUNTS[key]), "dataset_card_exact"
        return str(count), source

    if key in KNOWN_SPLIT_COUNTS:
        return str(KNOWN_SPLIT_COUNTS[key]), "dataset_card_exact"

    split_keys = discover_splits(meta)
    if len(split_keys) == 1:
        return str(parent_rows), "parent_single_split"

    return "", "not_public_per_split"


def build_split_row(meta, config, split):
    parent = meta["row"]
    name = parent["dataset_name"]
    is_agent = override_agent(parent, name, config, split)
    is_rl = truth(parent["is_rl"])
    is_code = override_code(parent, name, config, split)
    num_rows, num_rows_source = row_count(meta, config, split)

    filtered = parent["filtered_for_correctness"]
    verification = parent["includes_verification"]
    if not is_agent and not is_rl:
        filtered = ""
        verification = ""
    else:
        filtered = filtered if filtered != "" else "false"
        verification = verification if verification != "" else "false"

    encoded_config = urllib.parse.quote(config, safe="")
    encoded_split = urllib.parse.quote(split, safe="")
    split_url = f"https://huggingface.co/datasets/{name}?config={encoded_config}&split={encoded_split}"

    return {
        "dataset_name": name,
        "dataset_config": config,
        "split": split,
        "dataset_url": parent["dataset_url"],
        "split_url": split_url,
        "is_code_swe_terminal": bool_cell(is_code),
        "is_agent": bool_cell(is_agent),
        "is_rl": bool_cell(is_rl),
        "is_pretraining": bool_cell(truth(parent["is_pretraining"])),
        "reasoning": override_reasoning(parent, name, config, split),
        "filtered_for_correctness": filtered,
        "includes_verification": verification,
        "teacher_model": parent["teacher_model"],
        "aux_models": parent["aux_models"],
        "agent_harness": override_harness(parent, is_agent, name, config, split),
        "num_rows": num_rows,
        "num_rows_source": num_rows_source,
        "parent_num_rows": parent["num_rows"],
        "already_included": bool_cell(truth(parent["already_included"])),
    }


def generate(max_workers):
    parent_rows = read_parent_rows()
    metas = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_metadata, row) for row in parent_rows]
        for future in as_completed(futures):
            metas.append(future.result())
    metas.sort(key=lambda meta: parent_rows.index(meta["row"]))

    split_rows = []
    for meta in metas:
        for config, split in discover_splits(meta):
            split_rows.append(build_split_row(meta, config, split))
    return split_rows


def write_csv(rows, output_path):
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-workers", type=int, default=8)
    parser.add_argument("--output", type=Path, default=OUTPUT_CSV)
    args = parser.parse_args()

    rows = generate(args.max_workers)
    write_csv(rows, args.output)
    unknown_counts = sum(1 for row in rows if row["num_rows"] == "")
    print(f"wrote {len(rows)} split rows to {args.output}")
    print(f"rows with non-public per-split counts: {unknown_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
