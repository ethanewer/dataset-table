#!/usr/bin/env python3
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_CSV = ROOT / "split_datasets.csv"
OUTPUT_CSV = ROOT / "condensed_split_datasets.csv"

METADATA_COLUMNS = [
    "is_code_swe_terminal",
    "is_agent",
    "is_rl",
    "is_pretraining",
    "reasoning",
    "teacher_model",
    "aux_models",
    "agent_harness",
    "already_included",
]

OUTPUT_COLUMNS = [
    "readable_name",
    "dataset_name_regex",
    "hf_split_regex",
    "dataset_config_regex",
    *METADATA_COLUMNS,
    "num_rows_total",
    "num_rows_source",
    "covered_rows",
]

MAX_READABLE_NAME_CHARS = 64

ESTIMATED_NUM_ROWS_TOTAL = {
    # Dolmino split-level counts are not public for most component configs.
    # These are parent-row-count estimates weighted by repository file sizes.
    "Dolma3 Dolmino - code splits": "23016206",
    "Dolma3 Dolmino - 25 splits": "5132007803",
    # These grouped rows cover all public configs/splits for the dataset(s), so
    # the parent dataset row count is the best available total.
    "Nemotron Agentic v1 - agent/tool": "335122",
    "Nemotron CC - 9 splits": "8983613946",
    "Nemotron CC v2.1 - feedback splits": "3800016491",
    "Nemotron Competitive Programming v1 - 6 splits": "3927984",
    "Nemotron Pretrain Code - 7 splits": "1771380197",
    "Nemotron OpenCode SFT - 6 splits": "460254",
    # These rows split a parent dataset total; estimates are weighted by the
    # repository file sizes for the covered split files/directories.
    "Nemotron Pretrain SFT v1 - SFT Code": "56188967",
    "Nemotron Pretrain SFT v1 - SFT General, SFT Math": "243056050",
    "Nemotron IF Chat SFT v2 - no reasoning": "743044",
    "Nemotron IF Chat SFT v2 - reasoning": "1255524",
}


FAMILY_LABELS = {
    "allenai/dolma3_dolmino": "Dolma3 Dolmino",
    "allenai/dolma3_longmino": "Dolma3 Longmino",
    "allenai/dolma3": "Dolma3",
    "allenai/Sera": "Sera",
    "nvidia/Nemotron-Personas": "Nemotron Personas",
    "nvidia/Nemotron-Cascade": "Nemotron Cascade",
    "nvidia/Nemotron-Pretraining": "Nemotron Pretrain",
    "nvidia/Nemotron-CC": "Nemotron CC",
    "nvidia/OpenMath": "OpenMath",
}

DATASET_LABELS = {
    "AlienKevin/SWE-ZERO-12M-trajectories": "SWE-Zero 12M Trajectories",
    "Sellopale/OpenThoughts-Agent-v1-SFT": "OpenThoughts Agent SFT",
    "TeichAI/DeepSeek-v4-Pro-Agent": "DeepSeek Pro Agent",
    "allenai/dolma3_dolmino_mix-100B-1125": "Dolma3 Dolmino 100B 1125",
    "allenai/dolma3_dolmino_mix-10B-1025": "Dolma3 Dolmino 10B 1025",
    "allenai/dolma3_mix-150B-1025": "Dolma3 Mix 150B 1025",
    "lambda/hermes-agent-reasoning-traces": "Hermes Agent Traces",
    "nebius/SWE-agent-trajectories": "SWE Agent Trajectories",
    "open-thoughts/AgentTrove": "AgentTrove",
    "openbmb/UltraData-SFT-2605": "UltraData SFT 2605",
    "nvidia/AceReason-1.1-SFT": "AceReason SFT",
    "nvidia/HelpSteer3": "HelpSteer3",
    "nvidia/Llama-Nemotron-VLM-Dataset-v1": "Llama Nemotron VLM v1",
    "nvidia/Nemotron-VLM-Dataset-v2": "Nemotron VLM v2",
    "nvidia/Nemotron-3-Nano-RL-Training-Blend": "Nemotron 3 Nano RL Blend",
    "nvidia/Nemotron-Agentic-v1": "Nemotron Agentic v1",
    "nvidia/Nemotron-CC-Code-v1": "Nemotron CC Code v1",
    "nvidia/Nemotron-CC-v2.1": "Nemotron CC v2.1",
    "nvidia/Nemotron-Competitive-Programming-v1": "Nemotron Competitive Programming v1",
    "nvidia/Nemotron-CrossThink": "Nemotron CrossThink",
    "nvidia/Nemotron-Instruction-Following-Chat-v1": "Nemotron IF Chat v1",
    "nvidia/Nemotron-Math-HumanReasoning": "Nemotron Math HumanReasoning",
    "nvidia/Nemotron-Math-Proofs-v1": "Nemotron Math Proofs v1",
    "nvidia/Nemotron-Math-v2": "Nemotron Math v2",
    "nvidia/Nemotron-Pretraining-Dataset-sample": "Nemotron Pretrain Sample",
    "nvidia/Nemotron-Pretraining-SFT-v1": "Nemotron Pretrain SFT v1",
    "nvidia/Nemotron-Pretraining-Specialized-v1": "Nemotron Spec v1",
    "nvidia/Nemotron-Pretraining-Specialized-v1.1": "Nemotron Spec v1.1",
    "nvidia/Nemotron-PrismMath": "Nemotron PrismMath",
    "nvidia/Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1": "Nemotron RL Tool Use Pivot",
    "nvidia/Nemotron-RL-Agentic-Function-Calling-Pivot-v1": "Nemotron RL Function Pivot",
    "nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1": "Nemotron RL SWE Pivot",
    "nvidia/Nemotron-RL-Identity-Following-v1": "Nemotron RL Identity",
    "nvidia/Nemotron-RL-Instruction-Following-Adversarial-v1": "Nemotron RL Adversarial IF",
    "nvidia/Nemotron-RL-Instruction-Following-Calendar-v2": "Nemotron RL Calendar IF",
    "nvidia/Nemotron-RL-Instruction-Following-MultiTurnChat-v1": "Nemotron RL MultiTurnChat IF",
    "nvidia/Nemotron-RL-ReasoningGym-v1": "Nemotron RL ReasoningGym",
    "nvidia/Nemotron-RL-Safety-v1": "Nemotron RL Safety",
    "nvidia/Nemotron-RL-Super-Training-Blends": "Nemotron RL Super Blends",
    "nvidia/Nemotron-RL-agent-calendar_scheduling": "Nemotron RL Calendar Agent",
    "nvidia/Nemotron-RL-agent-workplace_assistant": "Nemotron RL Workplace Agent",
    "nvidia/Nemotron-RL-coding-competitive_coding": "Nemotron RL Competitive Coding",
    "nvidia/Nemotron-RL-instruction_following": "Nemotron RL IF",
    "nvidia/Nemotron-RL-instruction_following-structured_outputs": "Nemotron RL Structured Outputs",
    "nvidia/Nemotron-RLHF-GenRM-v1": "Nemotron RLHF GenRM",
    "nvidia/Nemotron-Research-GooseReason-0.7M": "GooseReason",
    "nvidia/Nemotron-SFT-Agentic-v2": "Nemotron Agentic SFT v2",
    "nvidia/Nemotron-SFT-Competitive-Programming-v2": "Nemotron CP SFT v2",
    "nvidia/Nemotron-SFT-Instruction-Following-Chat-v2": "Nemotron IF Chat SFT v2",
    "nvidia/Nemotron-SFT-Math-v3": "Nemotron Math SFT v3",
    "nvidia/Nemotron-SFT-Multilingual-v1": "Nemotron Multilingual SFT v1",
    "nvidia/Nemotron-SFT-OpenCode-v1": "Nemotron OpenCode SFT",
    "nvidia/Nemotron-SFT-SWE-v2": "Nemotron SWE SFT v2",
    "nvidia/Nemotron-SFT-Safety-v1": "Nemotron Safety SFT",
    "nvidia/Nemotron-SWE-v1": "Nemotron SWE v1",
    "nvidia/Nemotron-Science-v1": "Nemotron Science v1",
    "nvidia/Nemotron-SpecializedDomains-Finance-v1": "Nemotron Finance",
    "nvidia/Nemotron-Terminal-Corpus": "Nemotron Terminal Corpus",
    "nvidia/Nemotron-Terminal-Synthetic-Tasks": "Nemotron Terminal Tasks",
    "nvidia/OpenMathInstruct-1": "OpenMathInstruct 1",
    "nvidia/OpenMathInstruct-2": "OpenMathInstruct 2",
    "nvidia/SWE-Hero-openhands-trajectories": "SWE-Hero OpenHands",
    "nvidia/SWE-Zero-openhands-trajectories": "SWE-Zero OpenHands",
}

SPLIT_LABELS = {
    "agentless": "agentless",
    "chat_if": "chat IF",
    "code": "code",
    "conversational_agent": "conv agent",
    "cranecode": "CraneCode",
    "data": "data",
    "general": "general",
    "glm-5.1": "GLM 5.1",
    "interactive_agent": "interactive agent",
    "kimi": "Kimi",
    "lean": "Lean",
    "math": "math",
    "MCQ": "MCQ",
    "Nemotron-SFT-General": "SFT General",
    "Nemotron-SFT-MATH": "SFT Math",
    "no_think": "non-thinking",
    "openhands_swe": "OpenHands SWE",
    "reasoning_off": "no reasoning",
    "reasoning_on": "reasoning",
    "r2e_gym": "R2E Gym",
    "RQA": "RQA",
    "science": "science",
    "search": "search",
    "structured_outputs": "structured outputs",
    "swe": "SWE",
    "swe1": "SWE 1",
    "swe2": "SWE 2",
    "terminal_agent": "terminal agent",
    "think": "thinking",
    "tool_calling": "tool calling",
    "train_math": "math train",
    "train_qa": "QA train",
    "validation": "validation",
}

CODE_SPLIT_TOKENS = (
    "bash",
    "code",
    "coding",
    "cpp",
    "crane",
    "fim",
    "lean",
    "python",
    "scientific",
    "sql",
    "swe",
    "terminal",
)

VLM_SPLIT_TOKENS = (
    "caption",
    "chart",
    "diagram",
    "docvqa",
    "image",
    "ocr",
    "qa",
    "screen",
    "table",
    "video",
    "vision",
    "vlm",
    "vqa",
)


def read_rows(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def family_key(name):
    if name.startswith("allenai/dolma3_dolmino_"):
        return "allenai/dolma3_dolmino"
    if name.startswith("allenai/dolma3_longmino_"):
        return "allenai/dolma3_longmino"
    if name.startswith("allenai/dolma3_mix-") or name == "allenai/dolma3_pool":
        return "allenai/dolma3"
    if name.startswith("allenai/Sera-") or name.startswith("allenai/SERA-"):
        return "allenai/Sera"
    if name.startswith("nvidia/Nemotron-Personas-"):
        return "nvidia/Nemotron-Personas"
    if name.startswith("nvidia/Nemotron-Cascade-"):
        return "nvidia/Nemotron-Cascade"
    if name.startswith("nvidia/Nemotron-Pretraining-"):
        return "nvidia/Nemotron-Pretraining"
    if name.startswith("nvidia/Nemotron-CC-"):
        return "nvidia/Nemotron-CC"
    if name.startswith("nvidia/OpenMath"):
        return "nvidia/OpenMath"
    return name


def clean_token(value):
    label = SPLIT_LABELS.get(value)
    if label:
        return label
    label = re.sub(r"^(?:Nemotron-)+(?:Pretraining-)?", "", value)
    label = re.sub(r"^(?:Nemotron-)+(?:SFT-)?", "", label)
    label = label.replace("_", " ").replace("-", " ")
    label = re.sub(r"\s+", " ", label).strip()
    replacements = {
        "MATH": "math",
        "QA": "QA",
        "SFT": "SFT",
        "SWE": "SWE",
    }
    words = [replacements.get(word, word) for word in label.split()]
    return " ".join(words)


def family_label(family):
    if family in FAMILY_LABELS:
        return FAMILY_LABELS[family]
    return dataset_label(family)


def dataset_label(name):
    if name in DATASET_LABELS:
        return DATASET_LABELS[name]
    if name.startswith("allenai/"):
        label = name.removeprefix("allenai/")
    elif name.startswith("nvidia/"):
        label = name.removeprefix("nvidia/")
    else:
        label = name.split("/", 1)[-1]
    label = label.replace("_", " ").replace("-", " ")
    label = re.sub(r"\bDataset\b", "", label)
    label = re.sub(r"\s+", " ", label).strip()
    return label


def sera_group_label(dataset_names):
    if all("4.6-Lite" in name for name in dataset_names):
        if all(name.endswith("-T1") for name in dataset_names):
            return "Sera 4.6 Lite T1"
        if all(name.endswith("-T2") for name in dataset_names):
            return "Sera 4.6 Lite T2"
        if any("Best-Subset" in name for name in dataset_names) and len(dataset_names) == 1:
            return "Sera 4.6 Lite Best"
        return "Sera 4.6 Lite"
    if all("4.5A" in name for name in dataset_names):
        tier = ""
        if all(name.endswith("-T1") for name in dataset_names):
            tier = " T1"
        elif all(name.endswith("-T2") for name in dataset_names):
            tier = " T2"
        lower_names = [name.lower() for name in dataset_names]
        domains = []
        for domain in ("django", "full", "lite", "sphinx", "sympy"):
            if any(domain in name for name in lower_names):
                domains.append(domain)
        domain_label = "all domains" if len(domains) == 5 else "/".join(domains)
        if all(("sphinx" in name or "sympy" in name) for name in lower_names):
            return f"Sera 4.5A{tier} docs/math".strip()
        if domains:
            return f"Sera 4.5A{tier} {domain_label}".strip()
        return f"Sera 4.5A{tier}".strip()
    return "Sera"


def dataset_group_label(dataset_names, families):
    if len(dataset_names) == 1:
        return dataset_label(dataset_names[0])
    if len(families) == 1 and families[0] == "allenai/Sera":
        return sera_group_label(dataset_names)
    if len(families) == 1:
        return family_label(families[0])
    return f"{len(dataset_names)} datasets"


def split_category(split_names):
    split_names = sorted(set(split_names))
    if split_names == ["train"]:
        return ""
    if split_names == ["train", "validation"]:
        return "train/val"
    if split_names == ["general", "math", "science"]:
        return "general/math/science"
    if split_names == ["interactive_agent", "tool_calling"]:
        return "agent/tool"
    if split_names == ["interactive_agent", "search", "tool_calling"]:
        return "agent/search/tool"
    if len(split_names) == 1:
        split = split_names[0]
        if "/" in split:
            config, mode = split.rsplit("/", 1)
            return f"{clean_token(config)} {clean_token(mode)}"
        return clean_token(split)
    if all(split.endswith("/think") for split in split_names):
        return "thinking domains"
    if all(split.endswith("/no_think") for split in split_names):
        return "non-thinking domains"
    lower_names = [split.lower() for split in split_names]
    if all(any(token in split for token in CODE_SPLIT_TOKENS) for split in lower_names):
        return "code splits"
    if len(split_names) <= 3:
        return ", ".join(clean_token(split) for split in split_names)

    if all(any(token in split for token in VLM_SPLIT_TOKENS) for split in lower_names):
        return "VLM tasks"
    if all(re.search(r"(?:^|[_-])(agent|tool|swe|terminal)(?:$|[_-])", split) for split in lower_names):
        return "agent splits"
    if all(re.search(r"(?:france|korea|usa|persona|personas|language|country|region)", split) for split in lower_names):
        return "persona splits"
    if all(re.search(r"(?:helpsteer|preference|quality|response|conversation|prompt|score)", split) for split in lower_names):
        return "feedback splits"
    if all(re.search(r"(?:math|stem|science|reason|qa|flan|thought|crawl|wiki|reddit|train)", split) for split in lower_names):
        return "text/reasoning splits"
    return f"{len(split_names)} splits"


def readable_suffix(row):
    suffixes = []
    if row["is_rl"] == "True":
        suffixes.append("RL")
    elif row["is_agent"] == "True":
        suffixes.append("agent")
    elif row["is_code_swe_terminal"] == "True":
        suffixes.append("code")
    elif row["is_pretraining"] == "True":
        suffixes.append("pretrain")
    if row["num_rows_source"] != "dataset_server":
        suffixes.append(row["num_rows_source"].replace("_", " "))
    return ", ".join(suffixes[:2])


def regex_alt(values):
    values = sorted(set(values))
    if not values:
        return "^$"
    if len(values) == 1:
        return f"^{re.escape(values[0])}$"
    return "^(?:" + "|".join(re.escape(value) for value in values) + ")$"


def numeric_total(rows, column):
    total = 0
    for row in rows:
        value = row[column]
        if value == "":
            return ""
        total += int(value)
    return str(total)


def condensed_num_rows_total(group_rows, name):
    total = numeric_total(group_rows, "num_rows")
    if total:
        return total
    return ESTIMATED_NUM_ROWS_TOTAL.get(name, "")


def readable_name(group_rows):
    dataset_names = sorted({row["dataset_name"] for row in group_rows})
    split_names = sorted({row["hf_split"] for row in group_rows})
    families = sorted({family_key(name) for name in dataset_names})
    dataset_part = dataset_group_label(dataset_names, families)

    split_part = split_category(split_names)

    if split_part:
        return f"{dataset_part} - {split_part}"
    return dataset_part


def with_unique_readable_names(condensed):
    used = {}
    for row in condensed:
        base_name = row["readable_name"]
        candidate = base_name
        suffix = readable_suffix(row)
        if candidate in used and suffix:
            candidate = f"{base_name} ({suffix})"
        index = 2
        while candidate in used:
            candidate = f"{base_name} {index}"
            index += 1
        row["readable_name"] = candidate
        used[candidate] = True


def build_condensed_rows(rows):
    groups = defaultdict(list)
    for row in rows:
        key = (
            family_key(row["dataset_name"]),
            tuple(row[column] for column in METADATA_COLUMNS),
            row["num_rows_source"],
        )
        groups[key].append(row)

    condensed = []
    for (_family, metadata_values, num_rows_source), group_rows in sorted(
        groups.items(),
        key=lambda item: (
            min(row["dataset_name"] for row in item[1]),
            min(row["hf_split"] for row in item[1]),
            len(item[1]),
        ),
    ):
        name = readable_name(group_rows)
        row = {
            "readable_name": name,
            "dataset_name_regex": regex_alt(row["dataset_name"] for row in group_rows),
            "hf_split_regex": regex_alt(row["hf_split"] for row in group_rows),
            "dataset_config_regex": regex_alt(row["dataset_config"] for row in group_rows),
            "num_rows_total": condensed_num_rows_total(group_rows, name),
            "num_rows_source": num_rows_source,
            "covered_rows": str(len(group_rows)),
        }
        for column, value in zip(METADATA_COLUMNS, metadata_values):
            row[column] = value
        condensed.append(row)

    with_unique_readable_names(condensed)
    return condensed


def write_rows(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = read_rows(INPUT_CSV)
    condensed = build_condensed_rows(rows)
    write_rows(OUTPUT_CSV, condensed)
    print(f"wrote {len(condensed)} rows to {OUTPUT_CSV}")
    print(f"covered {sum(int(row['covered_rows']) for row in condensed)} source rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
