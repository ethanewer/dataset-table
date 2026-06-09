#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import json
import os
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


ROOT = Path("/wbl-fast/usrs/ee/code-swe-data")
TABLE = ROOT / "dataset-table" / "split_datasets.csv"
OUT_DIR = ROOT / "dataset-table" / "figures"
CSV_OUT = OUT_DIR / "mixed_reasoning_sample_estimates.csv"
JSON_OUT = OUT_DIR / "mixed_reasoning_sample_estimates.json"

SFT_ROOTS = (
    ROOT / "data" / "code-swe-terminal-agentic-sft",
    ROOT / "data" / "code-swe-terminal-non-agentic-sft",
)

QWEN_TOKENIZER = os.environ.get("QWEN_TOKENIZER", "Qwen/Qwen3-Coder-480B-A35B-Instruct")
NEMOTRON_TOKENIZER = os.environ.get("NEMOTRON_TOKENIZER", "nvidia/NVIDIA-Nemotron-Nano-12B-v2")
SAMPLE_ROWS = int(os.environ.get("MIXED_REASONING_SAMPLE_ROWS", "400"))
REMOTE_CHUNK_BYTES = int(os.environ.get("MIXED_REASONING_REMOTE_CHUNK_BYTES", str(4 * 1024 * 1024)))

TEACHER_REASONING = {
    "Qwen3-Coder-480B-A35B-Instruct": False,
    "DeepSeek-R1-0528": True,
    "DeepSeek-V3.2": True,
    "DeepSeek-V3.2-Speciale": True,
    "GPT-OSS-120B": True,
    "Qwen3-235B-A22B-Thinking-2507": True,
    "Qwen3-32B": True,
    "Qwen3-235B-A22B-Instruct-2507": False,
    "DeepSeek-V3": False,
    "DeepSeek-V3-0324": False,
    "Claude Opus 4.6": True,
    "claude-opus-4-6": True,
    "claude-opus-4-7": True,
}


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def under_sft_root(row: dict[str, str]) -> bool:
    local_path = row.get("local_path", "")
    return any(local_path.startswith(str(root)) for root in SFT_ROOTS)


def mixed_reasoning(row: dict[str, str]) -> bool:
    raw = (row.get("reasoning", "") or "").strip().lower()
    if not raw or raw in {"true", "false"}:
        return False
    try:
        parsed = json.loads(raw)
    except Exception:
        return "true" in raw and "false" in raw
    if not isinstance(parsed, list):
        return False
    values = [bool(value) for value in parsed]
    return any(values) and not all(values)


def stable_seed(*parts: str) -> int:
    text = "\n".join(parts)
    return sum((idx + 1) * ord(ch) for idx, ch in enumerate(text)) % (2**32)


def compact_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True, default=str)


def row_to_text(row: dict[str, Any]) -> str:
    priority = [
        "messages",
        "conversations",
        "conversation",
        "trajectory",
        "traces",
        "episodes",
        "prompt",
        "response",
        "completion",
        "text",
    ]
    picked: dict[str, Any] = {}
    for key in priority:
        if key in row and row[key] not in (None, "", [], {}):
            picked[key] = row[key]
    return compact_json(picked or row)


def parse_json_line(line: str) -> dict[str, Any] | None:
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except Exception:
        return None


def selected_files(row: dict[str, str]) -> tuple[list[Path], str]:
    path = Path(row["local_path"])
    name = row["dataset_name"]
    split = row["hf_split"]

    if name == "nvidia/Nemotron-SFT-SWE-v2":
        mapping = {
            "agentless": [path / "data" / "agentless.jsonl"],
            "openhands_swe": [path / "data" / "swe.jsonl"],
        }
        return [p for p in mapping.get(split, []) if p.exists()], "split_specific"

    if name == "nvidia/Nemotron-Cascade-2-SFT-Data":
        mapping = {
            "math": sorted((path / "math").glob("*.jsonl")),
            "science": sorted((path / "science").glob("*.jsonl")),
            "chat": sorted((path / "chat").glob("*.jsonl")),
            "instruction_following": sorted((path / "instruction_following").glob("*.jsonl")),
            "safety": sorted((path / "safety").glob("*.jsonl")),
            "conversational_agent": sorted((path / "conversational_agent").glob("*.jsonl")),
            "swe": sorted((path / "swe").glob("*.jsonl")),
            "terminal_agent": sorted((path / "terminal_agent").glob("*.jsonl")),
        }
        return [p for p in mapping.get(split, []) if p.exists()], "split_specific"

    if name == "nvidia/Nemotron-Cascade-SFT-Stage-2":
        mapping = {
            "code": sorted((path / "code").glob("*.jsonl")),
            "general": sorted((path / "general").glob("*.jsonl")),
            "instruction-following": [path / "instruction-following.jsonl"],
            "math": sorted((path / "math").glob("*.jsonl")),
            "science": [path / "science.jsonl"],
            "tool_calling": [path / "tool_calling.jsonl"],
            "swe_localization": [path / "swe_localization.jsonl"],
            "swe_repair": [path / "swe_repair.jsonl"],
            "swe_testgen": [path / "swe_testgen.jsonl"],
        }
        return [p for p in mapping.get(split, []) if p.exists()], "split_specific"

    if name == "Verdugie/opus-4.6-training-catalog":
        return sorted((path / "data").glob("*.jsonl")), "train_files"

    if name == "angrygiraffe/claude-opus-4.6-4.7-reasoning-8.7k":
        return sorted(path.glob("*train*.jsonl")), "train_files"

    return sorted(path.rglob("*.jsonl")), "fallback_jsonl"


def remote_paths(row: dict[str, str]) -> tuple[str, list[str]]:
    name = row["dataset_name"]
    split = row["hf_split"]
    if name == "nvidia/Nemotron-Cascade-2-SFT-Data":
        mapping = {
            "math": ["math/math_notool.jsonl", "math/math_proof.jsonl", "math/math_tool.jsonl"],
            "science": ["science/science.jsonl"],
            "chat": ["chat/chat_part_1.jsonl", "chat/chat_part_2.jsonl", "chat/chat_part_3.jsonl", "chat/chat_part_4.jsonl"],
            "instruction_following": ["instruction_following/instruction_following.jsonl"],
            "safety": ["safety/safety.jsonl"],
            "conversational_agent": ["conversational_agent/conversational_agent.jsonl"],
            "swe": ["swe/swe_agentic.jsonl", "swe/swe_agentless.jsonl"],
            "terminal_agent": ["terminal_agent/terminal_agent.jsonl"],
        }
        return name, mapping.get(split, [])
    if name == "nvidia/Nemotron-Cascade-SFT-Stage-2":
        mapping = {
            "code": [f"code/code_{idx}.jsonl" for idx in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]],
            "general": ["general/general_1.jsonl", "general/general_2.jsonl", "general/general_3.jsonl", "general/general_4.jsonl"],
            "instruction-following": ["instruction-following.jsonl"],
            "math": [f"math/math_{idx}.jsonl" for idx in range(1, 9)],
            "science": ["science.jsonl"],
            "tool_calling": ["tool_calling.jsonl"],
            "swe_localization": ["swe_localization.jsonl"],
            "swe_repair": ["swe_repair.jsonl"],
            "swe_testgen": ["swe_testgen.jsonl"],
        }
        return name, mapping.get(split, [])
    return "", []


def sample_jsonl_with_paths(files: list[Path], cap: int, seed: int) -> list[tuple[Path, dict[str, Any]]]:
    rng = random.Random(seed)
    samples: list[tuple[Path, dict[str, Any]]] = []
    if not files:
        return samples
    per_file = max(1, cap // len(files))
    for file in files:
        file_cap = min(per_file, cap - len(samples))
        if file_cap <= 0:
            break
        head_cap = max(1, min(file_cap, file_cap // 2))
        try:
            with file.open("r", encoding="utf-8", errors="replace") as f:
                for _ in range(head_cap):
                    obj = parse_json_line(f.readline())
                    if obj is not None:
                        samples.append((file, obj))
                        if len(samples) >= cap:
                            return samples
                size = file.stat().st_size
                for _ in range(file_cap - head_cap):
                    if size <= 0:
                        break
                    f.seek(rng.randrange(size))
                    f.readline()
                    obj = parse_json_line(f.readline())
                    if obj is not None:
                        samples.append((file, obj))
                        if len(samples) >= cap:
                            return samples
        except Exception:
            continue
    return samples[:cap]


def hf_url(repo_id: str, repo_path: str) -> str:
    from huggingface_hub import hf_hub_url

    return hf_hub_url(repo_id, repo_path, repo_type="dataset")


def read_remote_range(url: str, start: int, end: int) -> tuple[bytes, int | None]:
    req = Request(url, headers={"Range": f"bytes={start}-{end}", "User-Agent": "mixed-reasoning-sampler"})
    with urlopen(req, timeout=60) as response:
        data = response.read()
        total = None
        content_range = response.headers.get("Content-Range")
        if content_range and "/" in content_range:
            try:
                total = int(content_range.rsplit("/", 1)[1])
            except ValueError:
                total = None
        return data, total


def parse_jsonl_bytes(data: bytes, keep_first_partial: bool) -> list[dict[str, Any]]:
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    if not keep_first_partial and lines:
        lines = lines[1:]
    samples: list[dict[str, Any]] = []
    for line in lines:
        obj = parse_json_line(line)
        if obj is not None:
            samples.append(obj)
    return samples


def sample_remote_jsonl(repo_id: str, paths: list[str], cap: int, seed: int) -> list[tuple[str, dict[str, Any]]]:
    rng = random.Random(seed)
    samples: list[tuple[str, dict[str, Any]]] = []
    if not paths:
        return samples
    per_file = max(1, cap // len(paths))
    for repo_path in paths:
        if len(samples) >= cap:
            break
        url = hf_url(repo_id, repo_path)
        file_cap = min(per_file, cap - len(samples))
        try:
            head_bytes, total = read_remote_range(url, 0, REMOTE_CHUNK_BYTES - 1)
            candidates = parse_jsonl_bytes(head_bytes, keep_first_partial=True)
            if total and total > REMOTE_CHUNK_BYTES:
                try:
                    start = rng.randrange(max(1, total - REMOTE_CHUNK_BYTES))
                    end = min(total - 1, start + REMOTE_CHUNK_BYTES - 1)
                    chunk, _ = read_remote_range(url, start, end)
                    candidates.extend(parse_jsonl_bytes(chunk, keep_first_partial=False))
                except Exception:
                    pass
            if len(candidates) > file_cap:
                candidates = rng.sample(candidates, file_cap)
            for obj in candidates:
                samples.append((repo_path, obj))
                if len(samples) >= cap:
                    return samples
        except Exception:
            continue
    return samples[:cap]


def teacher_for_sample(row: dict[str, str], file: Path | str, obj: dict[str, Any]) -> str:
    name = row["dataset_name"]
    split = row["hf_split"]
    if name == "nvidia/Nemotron-SFT-SWE-v2":
        return "DeepSeek-R1-0528" if split == "agentless" else "Qwen3-Coder-480B-A35B-Instruct"
    for key in ("generator", "model", "teacher_model"):
        value = obj.get(key)
        if value:
            return str(value)
    if name == "Verdugie/opus-4.6-training-catalog":
        return "Claude Opus 4.6"
    if name == "angrygiraffe/claude-opus-4.6-4.7-reasoning-8.7k":
        return str(obj.get("model") or "Claude Opus 4.6/4.7")
    return "unknown"


def reasoning_for_sample(row: dict[str, str], file: Path | str, obj: dict[str, Any], teacher: str) -> bool:
    name = row["dataset_name"]
    if "thinking" in obj:
        return str(obj.get("thinking")).strip().lower() == "true"
    if name == "nvidia/Nemotron-SFT-SWE-v2":
        return row["hf_split"] == "agentless"
    if name == "Verdugie/opus-4.6-training-catalog":
        return str(obj.get("topic", "")).strip().lower() in {"reasoning", "coding"}
    if name == "angrygiraffe/claude-opus-4.6-4.7-reasoning-8.7k":
        return "_no_reasoning" not in Path(str(file)).name
    return TEACHER_REASONING.get(teacher, False)


def summarize_row(row: dict[str, str], qwen: Any, nemotron: Any) -> dict[str, Any]:
    files, source = selected_files(row)
    seed = stable_seed(row["dataset_name"], row["hf_split"], row.get("local_path", ""))
    samples: list[tuple[Path | str, dict[str, Any]]] = sample_jsonl_with_paths(files, SAMPLE_ROWS, seed)
    repo_id = ""
    remote = []
    if not samples:
        repo_id, remote = remote_paths(row)
        if repo_id and remote:
            samples = sample_remote_jsonl(repo_id, remote, SAMPLE_ROWS, seed)
            if samples:
                source = "remote_split_specific"
    result: dict[str, Any] = {
        "dataset_name": row["dataset_name"],
        "hf_split": row["hf_split"],
        "is_agent": row["is_agent"],
        "avg_estimated_tokens": int(row["avg_estimated_tokens"]),
        "reasoning": row["reasoning"],
        "teacher_model": row["teacher_model"],
        "file_selection": source,
        "files_sampled": [str(path.relative_to(Path(row["local_path"]))) for path in files] if files else remote,
        "sample_rows": len(samples),
        "sample_target_rows": SAMPLE_ROWS,
        "status": "sampled" if samples else "no_split_specific_files",
        "sample_notes": "" if samples else "No local or remote JSONL files matched this split; row remains unresolved in apportioned estimates.",
        "teachers": [],
        "reasoning_token_pct": None,
        "reasoning_row_pct": None,
    }
    if not samples:
        return result

    texts = [row_to_text(obj) for _, obj in samples]
    q_lens = [len(ids) for ids in qwen(texts, add_special_tokens=False)["input_ids"]]
    n_lens = [len(ids) for ids in nemotron(texts, add_special_tokens=False)["input_ids"]]
    sample_entries = []
    for (file, obj), q_len, n_len in zip(samples, q_lens, n_lens):
        teacher = teacher_for_sample(row, file, obj)
        is_reasoning = reasoning_for_sample(row, file, obj, teacher)
        sample_entries.append(
            {
                "teacher": teacher,
                "is_reasoning": is_reasoning,
                "tokens": (q_len + n_len) / 2,
            }
        )

    total_tokens = sum(entry["tokens"] for entry in sample_entries)
    total_rows = len(sample_entries)
    teacher_rows: dict[str, int] = defaultdict(int)
    teacher_tokens: dict[str, float] = defaultdict(float)
    reasoning_tokens = 0.0
    reasoning_rows = 0
    for entry in sample_entries:
        teacher_rows[entry["teacher"]] += 1
        teacher_tokens[entry["teacher"]] += entry["tokens"]
        if entry["is_reasoning"]:
            reasoning_tokens += entry["tokens"]
            reasoning_rows += 1

    teachers = []
    for teacher, token_sum in sorted(teacher_tokens.items(), key=lambda item: item[1], reverse=True):
        row_count = teacher_rows[teacher]
        teachers.append(
            {
                "teacher": teacher,
                "sample_rows": row_count,
                "sample_row_pct": row_count / total_rows if total_rows else 0,
                "sample_tokens": token_sum,
                "sample_token_pct": token_sum / total_tokens if total_tokens else 0,
                "estimated_row_tokens": round(int(row["avg_estimated_tokens"]) * (token_sum / total_tokens)) if total_tokens else 0,
            }
        )

    result["teachers"] = teachers
    result["reasoning_token_pct"] = reasoning_tokens / total_tokens if total_tokens else 0
    result["reasoning_row_pct"] = reasoning_rows / total_rows if total_rows else 0
    result["estimated_reasoning_tokens"] = round(int(row["avg_estimated_tokens"]) * result["reasoning_token_pct"])
    result["estimated_nonreasoning_tokens"] = int(row["avg_estimated_tokens"]) - result["estimated_reasoning_tokens"]
    location = "remote" if source == "remote_split_specific" else "local"
    file_count = len(remote) if source == "remote_split_specific" else len(files)
    result["sample_notes"] = f"Sampled {len(samples)} rows from {file_count} {location} split-specific JSONL file(s); token shares use mean Qwen/Nemotron token lengths."
    return result


def main() -> int:
    load_env()
    from transformers import AutoTokenizer

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with TABLE.open(newline="") as f:
        rows = [row for row in csv.DictReader(f) if under_sft_root(row) and mixed_reasoning(row)]

    qwen = AutoTokenizer.from_pretrained(QWEN_TOKENIZER, token=os.environ.get("HF_TOKEN") or None, use_fast=True)
    nemotron = AutoTokenizer.from_pretrained(NEMOTRON_TOKENIZER, token=os.environ.get("HF_TOKEN") or None, use_fast=True)

    results = []
    for idx, row in enumerate(rows, 1):
        result = summarize_row(row, qwen, nemotron)
        results.append(result)
        print(
            f"[{idx}/{len(rows)}] {row['dataset_name']} {row['hf_split']}: "
            f"{result['status']} samples={result['sample_rows']} reasoning_token_pct={result['reasoning_token_pct']}",
            flush=True,
        )

    JSON_OUT.write_text(json.dumps({"sample_rows_per_split": SAMPLE_ROWS, "results": results}, indent=2, sort_keys=True) + "\n")

    fieldnames = [
        "dataset_name",
        "hf_split",
        "is_agent",
        "status",
        "sample_rows",
        "avg_estimated_tokens",
        "teacher",
        "teacher_sample_rows",
        "teacher_row_pct",
        "teacher_token_pct",
        "teacher_estimated_tokens",
        "reasoning_token_pct",
        "estimated_reasoning_tokens",
        "files_sampled",
        "sample_notes",
    ]
    with CSV_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            if result["teachers"]:
                for teacher in result["teachers"]:
                    writer.writerow(
                        {
                            "dataset_name": result["dataset_name"],
                            "hf_split": result["hf_split"],
                            "is_agent": result["is_agent"],
                            "status": result["status"],
                            "sample_rows": result["sample_rows"],
                            "avg_estimated_tokens": result["avg_estimated_tokens"],
                            "teacher": teacher["teacher"],
                            "teacher_sample_rows": teacher["sample_rows"],
                            "teacher_row_pct": f"{teacher['sample_row_pct']:.6f}",
                            "teacher_token_pct": f"{teacher['sample_token_pct']:.6f}",
                            "teacher_estimated_tokens": teacher["estimated_row_tokens"],
                            "reasoning_token_pct": f"{result['reasoning_token_pct']:.6f}",
                            "estimated_reasoning_tokens": result["estimated_reasoning_tokens"],
                            "files_sampled": ";".join(result["files_sampled"]),
                            "sample_notes": result["sample_notes"],
                        }
                    )
            else:
                writer.writerow(
                    {
                        "dataset_name": result["dataset_name"],
                        "hf_split": result["hf_split"],
                        "is_agent": result["is_agent"],
                        "status": result["status"],
                        "sample_rows": result["sample_rows"],
                        "avg_estimated_tokens": result["avg_estimated_tokens"],
                        "teacher": "",
                        "teacher_sample_rows": "",
                        "teacher_row_pct": "",
                        "teacher_token_pct": "",
                        "teacher_estimated_tokens": "",
                        "reasoning_token_pct": "",
                        "estimated_reasoning_tokens": "",
                        "files_sampled": ";".join(result["files_sampled"]),
                        "sample_notes": result["sample_notes"],
                    }
                )

    print(f"wrote {CSV_OUT}")
    print(f"wrote {JSON_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
