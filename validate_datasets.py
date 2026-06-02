#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "datasets.csv"

COLUMNS = [
    "dataset_name",
    "dataset_url",
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
    "already_included",
]

OLMO3_COLLECTION_ROWS = {
    "allenai/Dolci-Think-SFT-7B": 2268178,
    "allenai/Dolci-Think-DPO-7B": 150000,
    "allenai/Dolci-Think-RL-7B": 102014,
    "allenai/Dolci-Think-SFT-32B": 2253684,
    "allenai/Dolci-Think-DPO-32B": 200000,
    "allenai/Dolci-Think-RL-32B": 102026,
    "allenai/Dolci-Think-SFT-Python": 1090000,
    "allenai/Dolci-Instruct-SFT": 2152112,
    "allenai/Dolci-Instruct-DPO": 259922,
    "allenai/Dolci-Instruct-RL": 169964,
    "allenai/Dolci-RL-Zero-IF-7B": 13179,
    "allenai/Dolci-RL-Zero-Math-7B": 13314,
    "allenai/Dolci-RL-Zero-Code-7B": 13312,
    "allenai/Dolci-RL-Zero-General-7B": 12841,
    "allenai/Dolci-RL-Zero-Mix-7B": 46931,
    "allenai/Dolci-Instruct-SFT-No-Tools": 1924533,
    "allenai/Dolci-Instruct-SFT-Tool-Use": 227579,
    "allenai/Dolci-Instruct-SFT-Tool-Use-SA": 1604,
    "allenai/dolma3_pool": 9970000000,
    "allenai/dolma3_dolmino_pool": 2520000000,
    "allenai/dolma3_longmino_pool": 22300000,
    "allenai/dolma3_dolmino_mix-100B-1025": 14091980,
    "allenai/dolma3_longmino_mix-50B-1025": 80000000,
    "allenai/dolma3_dolmino_mix-10B-1025": 5037781,
    "allenai/dolma3_mix-150B-1025": 89281027,
    "allenai/dolma3_dolmino_mix-100B-1125": 0,
    "allenai/dolma3_longmino_mix-100B-1125": 0,
    "allenai/dolma3_mix-6T-1025-7B": 3870000000,
}

OPEN_CODING_AGENTS_ROWS = {
    "allenai/Sera-4.6-Lite-T2": 36083,
    "allenai/Sera-4.5A-Lite-T1": 36607,
    "allenai/SERA-4.6-Lite-Best-Subset": 47498,
    "allenai/Sera-4.5A-Lite-T2": 35615,
    "allenai/Sera-4.5A-Full-T1": 72118,
    "allenai/Sera-4.5A-Full-T2": 66337,
    "allenai/Sera-4.6-Lite-T1": 36825,
    "allenai/Sera-4.5A-Django-T1": 24218,
    "allenai/Sera-4.5A-Django-T2": 21900,
    "allenai/Sera-4.5A-Sympy-T1": 27227,
    "allenai/Sera-4.5A-Sympy-T2": 25397,
    "allenai/Sera-4.5A-Sphinx-T1": 24553,
    "allenai/Sera-4.5A-Sphinx-T2": 12676,
}

NEMOTRON_PRETRAINING_ROWS = {
    "nvidia/Nemotron-Pretraining-Dataset-sample": 27706,
    "nvidia/Nemotron-Pretraining-Specialized-v1.1": 19772096,
    "nvidia/Nemotron-CC-Code-v1": 216347017,
    "nvidia/Nemotron-CC-v2.1": 3800016491,
    "nvidia/Nemotron-Pretraining-Code-v2": 835834532,
    "nvidia/Nemotron-Pretraining-Specialized-v1": 60655840,
    "nvidia/Nemotron-CC-Math-v1": 189875695,
    "nvidia/Nemotron-CC-v2": 8793738251,
    "nvidia/Nemotron-Pretraining-SFT-v1": 299245017,
    "nvidia/Nemotron-Pretraining-Code-v1": 935545665,
}

NEMOTRON_POST_TRAINING_V3_ROWS = {
    "nvidia/Nemotron-3-Nano-RL-Training-Blend": 93244,
    "nvidia/Nemotron-Science-v1": 226334,
    "nvidia/Nemotron-Instruction-Following-Chat-v1": 430978,
    "nvidia/Nemotron-Math-Proofs-v1": 1376666,
    "nvidia/Nemotron-Agentic-v1": 335122,
    "nvidia/Nemotron-Competitive-Programming-v1": 3927984,
    "nvidia/Nemotron-Math-v2": 7085839,
    "nvidia/Nemotron-SWE-v1": 51029,
    "nvidia/Nemotron-SFT-SWE-v2": 256254,
    "nvidia/Nemotron-SFT-Safety-v1": 45145,
    "nvidia/Nemotron-SFT-Competitive-Programming-v2": 844935,
    "nvidia/Nemotron-SpecializedDomains-Finance-v1": 326698,
    "nvidia/Nemotron-SFT-Math-v3": 3638783,
    "nvidia/Nemotron-SFT-Instruction-Following-Chat-v2": 1998568,
    "nvidia/Nemotron-RLHF-GenRM-v1": 299517,
    "nvidia/Nemotron-RL-ReasoningGym-v1": 15000,
    "nvidia/Nemotron-SFT-Multilingual-v1": 3065255,
    "nvidia/Nemotron-RL-Safety-v1": 89068,
    "nvidia/Nemotron-RL-Identity-Following-v1": 21660,
    "nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1": 50308,
    "nvidia/Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1": 96968,
    "nvidia/Nemotron-RL-Agentic-Function-Calling-Pivot-v1": 9620,
    "nvidia/Nemotron-RL-Instruction-Following-Adversarial-v1": 1000,
    "nvidia/Nemotron-RL-Instruction-Following-MultiTurnChat-v1": 2011,
    "nvidia/Nemotron-RL-Instruction-Following-Calendar-v2": 9915,
    "nvidia/Nemotron-RL-Super-Training-Blends": 479303,
    "nvidia/Nemotron-SFT-Agentic-v2": 991900,
    "nvidia/Nemotron-SFT-OpenCode-v1": 460254,
}

NEMOTRON_SUPERVISED_FINE_TUNING_ROWS = {
    "nvidia/Nemotron-SFT-Math-v3": 3638783,
    "nvidia/Nemotron-SFT-Agentic-v2": 991900,
    "nvidia/Nemotron-SFT-Competitive-Programming-v2": 844935,
    "nvidia/Nemotron-SFT-Instruction-Following-Chat-v2": 1998568,
    "nvidia/Nemotron-SFT-Multilingual-v1": 3065255,
    "nvidia/Nemotron-SFT-OpenCode-v1": 460254,
    "nvidia/Nemotron-SFT-Safety-v1": 45145,
    "nvidia/Nemotron-SFT-SWE-v2": 256254,
    "nvidia/Nemotron-SpecializedDomains-Finance-v1": 326698,
    "nvidia/Nemotron-Instruction-Following-Chat-v1": 430978,
    "nvidia/Nemotron-Agentic-v1": 335122,
    "nvidia/Nemotron-SWE-v1": 51029,
    "nvidia/Nemotron-Competitive-Programming-v1": 3927984,
    "nvidia/Nemotron-Math-v2": 7085839,
    "nvidia/Nemotron-Math-Proofs-v1": 1376666,
    "nvidia/Nemotron-Math-HumanReasoning": 250,
    "nvidia/Nemotron-PrismMath": 1002595,
    "nvidia/Nemotron-CrossThink": 287376,
    "nvidia/Nemotron-Research-GooseReason-0.7M": 673125,
    "nvidia/AceReason-1.1-SFT": 3970332,
    "nvidia/Llama-Nemotron-VLM-Dataset-v1": 2863834,
    "nvidia/Nemotron-VLM-Dataset-v2": 8147599,
    "nvidia/Nemotron-Cascade-2-SFT-Data": 24824269,
    "nvidia/Nemotron-Cascade-SFT-Stage-1": 5436618,
    "nvidia/Nemotron-Cascade-SFT-Stage-2": 7797730,
    "nvidia/Nemotron-Cascade-SFT-SWE": 162262,
    "nvidia/Nemotron-Science-v1": 226334,
    "nvidia/OpenMathInstruct-1": 6879694,
    "nvidia/OpenMathInstruct-2": 21972791,
    "nvidia/OpenMath-GSM8K-masked": 7473,
    "nvidia/OpenMath-MATH-masked": 7500,
    "nvidia/Nemotron-Personas-USA": 1000000,
    "nvidia/Nemotron-Personas-Brazil": 1000000,
    "nvidia/Nemotron-Personas-France": 1000000,
    "nvidia/Nemotron-Personas-India": 3000000,
    "nvidia/Nemotron-Personas-Japan": 1000000,
    "nvidia/Nemotron-Personas-Korea": 1000000,
    "nvidia/Nemotron-Personas-Singapore": 148000,
}

NVIDIA_SWE_ZERO_TO_HERO_ROWS = {
    "nvidia/SWE-Zero-openhands-trajectories": 318115,
    "nvidia/SWE-Hero-openhands-trajectories": 34269,
}

NEMOTRON_AGENTIC_AND_TOOL_USE_ROWS = {
    "nvidia/Nemotron-SFT-Agentic-v2": 991900,
    "nvidia/Nemotron-Agentic-v1": 335122,
    "nvidia/Nemotron-RL-agent-calendar_scheduling": 4000,
    "nvidia/Nemotron-RL-agent-workplace_assistant": 1800,
    "nvidia/Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1": 96968,
    "nvidia/Nemotron-RL-Agentic-Function-Calling-Pivot-v1": 9620,
    "nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1": 50308,
    "nvidia/Nemotron-Terminal-Corpus": 366154,
    "nvidia/Nemotron-Terminal-Synthetic-Tasks": 0,
}

NEMOTRON_CHAT_INSTRUCTION_ROWS = {
    "nvidia/Nemotron-SFT-Instruction-Following-Chat-v2": 1998568,
    "nvidia/Nemotron-Instruction-Following-Chat-v1": 430978,
    "nvidia/Nemotron-SFT-Multilingual-v1": 3065255,
    "nvidia/Nemotron-RL-instruction_following": 46391,
    "nvidia/Nemotron-RL-instruction_following-structured_outputs": 9949,
    "nvidia/Nemotron-RL-Identity-Following-v1": 21660,
    "nvidia/Nemotron-RL-Instruction-Following-Adversarial-v1": 1000,
    "nvidia/Nemotron-RL-Instruction-Following-Calendar-v2": 9915,
    "nvidia/Nemotron-RL-Instruction-Following-MultiTurnChat-v1": 2011,
    "nvidia/Nemotron-Cascade-RL-Instruction-Following": 108938,
    "nvidia/HelpSteer3": 132937,
}

NEMOTRON_CODE_SWE_ROWS = {
    "nvidia/Nemotron-SFT-Competitive-Programming-v2": 844935,
    "nvidia/Nemotron-SFT-OpenCode-v1": 460254,
    "nvidia/Nemotron-SFT-SWE-v2": 256254,
    "nvidia/Nemotron-SWE-v1": 51029,
    "nvidia/Nemotron-Competitive-Programming-v1": 3927984,
    "nvidia/Nemotron-RL-coding-competitive_coding": 16083,
    "nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1": 50308,
    "nvidia/Nemotron-Cascade-RL-SWE": 109996,
    "nvidia/Nemotron-Cascade-SFT-SWE": 162262,
    "nvidia/Nemotron-CC-Code-v1": 216347017,
    "nvidia/Nemotron-Pretraining-Code-v1": 935545665,
    "nvidia/Nemotron-Pretraining-Code-v2": 835834532,
}

PRETRAINING_TRUE = {
    "allenai/dolma3_pool",
    "allenai/dolma3_dolmino_pool",
    "allenai/dolma3_longmino_pool",
    "allenai/dolma3_dolmino_mix-100B-1025",
    "allenai/dolma3_longmino_mix-50B-1025",
    "allenai/dolma3_dolmino_mix-10B-1025",
    "allenai/dolma3_mix-150B-1025",
    "allenai/dolma3_dolmino_mix-100B-1125",
    "allenai/dolma3_longmino_mix-100B-1125",
    "allenai/dolma3_mix-6T-1025-7B",
    "nvidia/Nemotron-Pretraining-Dataset-sample",
    "nvidia/Nemotron-Pretraining-Specialized-v1.1",
    "nvidia/Nemotron-CC-Code-v1",
    "nvidia/Nemotron-CC-v2.1",
    "nvidia/Nemotron-Pretraining-Code-v2",
    "nvidia/Nemotron-Pretraining-Specialized-v1",
    "nvidia/Nemotron-CC-Math-v1",
    "nvidia/Nemotron-CC-v2",
    "nvidia/Nemotron-Pretraining-Code-v1",
}

AGENT_TRUE = {
    "nvidia/Nemotron-3-Nano-RL-Training-Blend",
    "nvidia/Nemotron-Agentic-v1",
    "nvidia/Nemotron-SWE-v1",
    "nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1",
    "nvidia/Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1",
    "nvidia/Nemotron-RL-Agentic-Function-Calling-Pivot-v1",
    "nvidia/Nemotron-RL-Super-Training-Blends",
    "nvidia/Nemotron-Cascade-2-SFT-Data",
    "nvidia/Nemotron-Cascade-SFT-Stage-2",
    "nvidia/SWE-Zero-openhands-trajectories",
    "nvidia/SWE-Hero-openhands-trajectories",
    "nvidia/Nemotron-RL-agent-workplace_assistant",
    "nvidia/Nemotron-Terminal-Synthetic-Tasks",
    "nvidia/Nemotron-SFT-OpenCode-v1",
    "nvidia/Nemotron-Terminal-Corpus",
    "nvidia/Nemotron-SFT-Agentic-v2",
    "nvidia/Nemotron-SFT-SWE-v2",
    "allenai/Sera-4.6-Lite-T2",
    "allenai/Sera-4.5A-Lite-T1",
    "allenai/SERA-4.6-Lite-Best-Subset",
    "allenai/Sera-4.5A-Lite-T2",
    "allenai/Sera-4.5A-Full-T1",
    "allenai/Sera-4.5A-Full-T2",
    "allenai/Sera-4.6-Lite-T1",
    "allenai/Sera-4.5A-Django-T1",
    "allenai/Sera-4.5A-Django-T2",
    "allenai/Sera-4.5A-Sympy-T1",
    "allenai/Sera-4.5A-Sympy-T2",
    "allenai/Sera-4.5A-Sphinx-T1",
    "allenai/Sera-4.5A-Sphinx-T2",
    "Sellopale/OpenThoughts-Agent-v1-SFT",
    "lambda/hermes-agent-reasoning-traces",
    "TeichAI/DeepSeek-v4-Pro-Agent",
    "open-thoughts/AgentTrove",
    "nebius/SWE-agent-trajectories",
    "AlienKevin/SWE-ZERO-12M-trajectories",
}

RL_TRUE = {
    "nvidia/Nemotron-3-Nano-RL-Training-Blend",
    "nvidia/Nemotron-RLHF-GenRM-v1",
    "nvidia/Nemotron-RL-ReasoningGym-v1",
    "nvidia/Nemotron-RL-Safety-v1",
    "nvidia/Nemotron-RL-Identity-Following-v1",
    "nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1",
    "nvidia/Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1",
    "nvidia/Nemotron-RL-Agentic-Function-Calling-Pivot-v1",
    "nvidia/Nemotron-RL-Instruction-Following-Adversarial-v1",
    "nvidia/Nemotron-RL-Instruction-Following-MultiTurnChat-v1",
    "nvidia/Nemotron-RL-Instruction-Following-Calendar-v2",
    "nvidia/Nemotron-RL-Super-Training-Blends",
    "nvidia/Nemotron-CrossThink",
    "nvidia/Nemotron-Research-GooseReason-0.7M",
    "nvidia/Nemotron-RL-agent-calendar_scheduling",
    "nvidia/Nemotron-RL-agent-workplace_assistant",
    "nvidia/Nemotron-Terminal-Synthetic-Tasks",
    "nvidia/Nemotron-RL-instruction_following",
    "nvidia/Nemotron-RL-instruction_following-structured_outputs",
    "nvidia/Nemotron-Cascade-RL-Instruction-Following",
    "nvidia/HelpSteer3",
    "nvidia/Nemotron-RL-coding-competitive_coding",
    "nvidia/Nemotron-Cascade-RL-SWE",
    "allenai/Dolci-Think-RL-7B",
    "allenai/Dolci-Think-RL-32B",
    "allenai/Dolci-Instruct-RL",
    "allenai/Dolci-RL-Zero-IF-7B",
    "allenai/Dolci-RL-Zero-Math-7B",
    "allenai/Dolci-RL-Zero-Code-7B",
    "allenai/Dolci-RL-Zero-General-7B",
    "allenai/Dolci-RL-Zero-Mix-7B",
}

CODE_SWE_TERMINAL_TRUE = {
    "nvidia/Nemotron-Competitive-Programming-v1",
    "nvidia/Nemotron-SWE-v1",
    "nvidia/Nemotron-RL-Agentic-SWE-Pivot-v1",
    "nvidia/Nemotron-Cascade-SFT-SWE",
    "nvidia/SWE-Zero-openhands-trajectories",
    "nvidia/SWE-Hero-openhands-trajectories",
    "nvidia/Nemotron-Terminal-Synthetic-Tasks",
    "nvidia/Nemotron-RL-coding-competitive_coding",
    "nvidia/Nemotron-Cascade-RL-SWE",
    "nvidia/Nemotron-SFT-Competitive-Programming-v2",
    "nvidia/Nemotron-SFT-OpenCode-v1",
    "nvidia/Nemotron-Terminal-Corpus",
    "nvidia/Nemotron-SFT-SWE-v2",
    "nvidia/Nemotron-Pretraining-Specialized-v1.1",
    "nvidia/Nemotron-CC-Code-v1",
    "nvidia/Nemotron-Pretraining-Code-v2",
    "nvidia/Nemotron-Pretraining-Code-v1",
    "allenai/Dolci-Think-SFT-Python",
    "allenai/Dolci-RL-Zero-Code-7B",
    "allenai/Sera-4.6-Lite-T2",
    "allenai/Sera-4.5A-Lite-T1",
    "allenai/SERA-4.6-Lite-Best-Subset",
    "allenai/Sera-4.5A-Lite-T2",
    "allenai/Sera-4.5A-Full-T1",
    "allenai/Sera-4.5A-Full-T2",
    "allenai/Sera-4.6-Lite-T1",
    "allenai/Sera-4.5A-Django-T1",
    "allenai/Sera-4.5A-Django-T2",
    "allenai/Sera-4.5A-Sympy-T1",
    "allenai/Sera-4.5A-Sympy-T2",
    "allenai/Sera-4.5A-Sphinx-T1",
    "allenai/Sera-4.5A-Sphinx-T2",
    "Sellopale/OpenThoughts-Agent-v1-SFT",
    "lambda/hermes-agent-reasoning-traces",
    "TeichAI/DeepSeek-v4-Pro-Agent",
    "open-thoughts/AgentTrove",
    "nebius/SWE-agent-trajectories",
    "AlienKevin/SWE-ZERO-12M-trajectories",
}


def parse_json_cell(row, column, errors):
    value = row[column]
    if not value:
        return None
    if value[0] not in "[{":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        errors.append(f"{row['dataset_name']}: {column} is invalid JSON: {exc}")
        return None


def main():
    errors = []
    with CSV_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if reader.fieldnames != COLUMNS:
            errors.append("CSV header does not match schema columns")

    by_name = {}
    for row in rows:
        name = row["dataset_name"]
        if name in by_name:
            errors.append(f"duplicate dataset_name: {name}")
        by_name[name] = row

        expected_url = f"https://huggingface.co/datasets/{name}"
        if row["dataset_url"] != expected_url:
            errors.append(f"{name}: dataset_url should be {expected_url}")

        for column in [
            "is_code_swe_terminal",
            "is_agent",
            "is_rl",
            "is_pretraining",
            "already_included",
        ]:
            if row[column] not in {"true", "false"}:
                errors.append(f"{name}: {column} must be true or false")

        for column in ["filtered_for_correctness", "includes_verification"]:
            if row[column] not in {"", "true", "false"}:
                errors.append(f"{name}: {column} must be blank, true, or false")

        try:
            if int(row["num_rows"]) < 0:
                errors.append(f"{name}: num_rows must be non-negative")
        except ValueError:
            errors.append(f"{name}: num_rows must be an integer")

        teacher = parse_json_cell(row, "teacher_model", errors)
        reasoning = parse_json_cell(row, "reasoning", errors)
        aux = parse_json_cell(row, "aux_models", errors)

        if row["reasoning"] not in {"true", "false"} and reasoning is None:
            errors.append(f"{name}: reasoning must be true, false, or a JSON list")
        if isinstance(teacher, list):
            if not isinstance(reasoning, list):
                errors.append(f"{name}: JSON-list teacher_model requires JSON-list reasoning")
            elif len(teacher) != len(reasoning):
                errors.append(f"{name}: teacher_model and reasoning list lengths differ")
        if aux is not None:
            if not isinstance(aux, list):
                errors.append(f"{name}: aux_models must be a JSON array")
            elif not all(isinstance(item, dict) and "model" in item and "use" in item for item in aux):
                errors.append(f"{name}: aux_models entries must contain model and use")

    collection_rows = {
        **OLMO3_COLLECTION_ROWS,
        **OPEN_CODING_AGENTS_ROWS,
        **NEMOTRON_PRETRAINING_ROWS,
        **NEMOTRON_POST_TRAINING_V3_ROWS,
        **NEMOTRON_SUPERVISED_FINE_TUNING_ROWS,
        **NVIDIA_SWE_ZERO_TO_HERO_ROWS,
        **NEMOTRON_AGENTIC_AND_TOOL_USE_ROWS,
        **NEMOTRON_CHAT_INSTRUCTION_ROWS,
        **NEMOTRON_CODE_SWE_ROWS,
    }

    missing = sorted(set(collection_rows) - set(by_name))
    if missing:
        errors.append("missing required collection datasets: " + ", ".join(missing))

    for name, expected_rows in collection_rows.items():
        row = by_name.get(name)
        if row and int(row["num_rows"]) != expected_rows:
            errors.append(f"{name}: expected num_rows {expected_rows}, found {row['num_rows']}")

    for name in PRETRAINING_TRUE:
        row = by_name.get(name)
        if row and row["is_pretraining"] != "true":
            errors.append(f"{name}: expected is_pretraining=true")
    for name, row in by_name.items():
        if name not in PRETRAINING_TRUE and row["is_pretraining"] != "false":
            errors.append(f"{name}: expected is_pretraining=false")

    for name in AGENT_TRUE:
        row = by_name.get(name)
        if row and row["is_agent"] != "true":
            errors.append(f"{name}: expected is_agent=true")
    for name, row in by_name.items():
        if name not in AGENT_TRUE and row["is_agent"] != "false":
            errors.append(f"{name}: expected is_agent=false")

    for name in RL_TRUE:
        row = by_name.get(name)
        if row and row["is_rl"] != "true":
            errors.append(f"{name}: expected is_rl=true")
    for name, row in by_name.items():
        if name not in RL_TRUE and row["is_rl"] != "false":
            errors.append(f"{name}: expected is_rl=false")

    for name in CODE_SWE_TERMINAL_TRUE:
        row = by_name.get(name)
        if row and row["is_code_swe_terminal"] != "true":
            errors.append(f"{name}: expected is_code_swe_terminal=true")
    for name, row in by_name.items():
        if name not in CODE_SWE_TERMINAL_TRUE and row["is_code_swe_terminal"] != "false":
            errors.append(f"{name}: expected is_code_swe_terminal=false")

    for row in by_name.values():
        if row["is_agent"] == "true" or row["is_rl"] == "true":
            if row["filtered_for_correctness"] == "":
                errors.append(f"{row['dataset_name']}: filtered_for_correctness is required for agent/RL rows")
            if row["includes_verification"] == "":
                errors.append(f"{row['dataset_name']}: includes_verification is required for agent/RL rows")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(
        f"ok: {len(rows)} rows; "
        f"{len(OLMO3_COLLECTION_ROWS)} OLMo 3 collection datasets present; "
        f"{len(OPEN_CODING_AGENTS_ROWS)} Open Coding Agents datasets present; "
        f"{len(NEMOTRON_PRETRAINING_ROWS)} Nemotron pretraining datasets present; "
        f"{len(NEMOTRON_POST_TRAINING_V3_ROWS)} Nemotron post-training v3 datasets present; "
        f"{len(NEMOTRON_SUPERVISED_FINE_TUNING_ROWS)} Nemotron SFT datasets present; "
        f"{len(NVIDIA_SWE_ZERO_TO_HERO_ROWS)} SWE Zero-to-Hero datasets present; "
        f"{len(NEMOTRON_AGENTIC_AND_TOOL_USE_ROWS)} Nemotron agentic/tool-use datasets present; "
        f"{len(NEMOTRON_CHAT_INSTRUCTION_ROWS)} Nemotron chat/instruction datasets present; "
        f"{len(NEMOTRON_CODE_SWE_ROWS)} Nemotron code/SWE datasets present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
