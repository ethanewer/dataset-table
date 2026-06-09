#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path("/wbl-fast/usrs/ee/code-swe-data")
TABLE = ROOT / "dataset-table" / "split_datasets.csv"
OUT_DIR = ROOT / "dataset-table" / "figures"
OUTPUT = OUT_DIR / "sft_token_overview.svg"
MIXED_SAMPLE_JSON = OUT_DIR / "mixed_reasoning_sample_estimates.json"

SFT_ROOTS = (
    ROOT / "data" / "code-swe-terminal-agentic-sft",
    ROOT / "data" / "code-swe-terminal-non-agentic-sft",
)

OBSOLETE_FIGURES = (
    "agentic_sft_tokens_by_teacher.svg",
    "non_agentic_sft_tokens_by_teacher.svg",
    "agentic_sft_tokens_by_harness.svg",
    "sft_reasoning_vs_nonreasoning_tokens.svg",
)

REASONING_CATEGORIES = (
    ("Reasoning", "#2f6f73"),
    ("Non-reasoning", "#6b7280"),
    ("Unresolved mixed", "#c58b2b"),
)


def is_under_sft_root(row: dict[str, str]) -> bool:
    local_path = row.get("local_path", "")
    return any(local_path.startswith(str(root)) for root in SFT_ROOTS)


def token_count(row: dict[str, str]) -> int:
    value = row.get("avg_estimated_tokens", "")
    return int(value) if value and value.isdigit() else 0


def load_rows() -> list[dict[str, str]]:
    with TABLE.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return [row for row in rows if is_under_sft_root(row) and token_count(row) > 0]


def compact_tokens(value: int) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs_value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def percent(value: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{100 * value / total:.1f}%"


def short_model_name(name: str) -> str:
    return name.split("/")[-1].replace("_", " ")


def display_label(raw: str, default: str) -> str:
    raw = (raw or "").strip() or default
    return raw


def trunc(text: str, max_chars: int) -> str:
    return text if len(text) <= max_chars else text[: max_chars - 3].rstrip() + "..."


def agent_label(row: dict[str, str]) -> str:
    return "Agentic" if row.get("is_agent") == "true" else "Non-agentic"


def normalize_teacher_name(raw: str) -> str:
    raw = (raw or "").strip() or "not_specified"
    lower = raw.lower()
    if lower in {"", "-", "n/a", "na", "none", "null", "not_specified", "unknown"}:
        return "Unknown teacher"
    if "claude" in lower or "opus" in lower:
        return "Claude / Opus"
    if "glm-4.6" in lower:
        return "GLM-4.6"
    if "glm-4.7" in lower:
        return "GLM-4.7"
    if "glm-5.1" in lower:
        return "GLM-5.1"
    if "glm-5.0" in lower:
        return "GLM-5.0"
    if "kimi-k2.5" in lower or "kimi k2.5" in lower:
        return "Kimi-K2.5"
    if "kimi-2.5" in lower or "kimi 2.5" in lower:
        return "Kimi-2.5"
    if "minimax-m2.7" in lower or "minimax m2.7" in lower:
        return "MiniMax-M2.7"
    if "minimax m2.0" in lower or "minimax-m2.0" in lower:
        return "MiniMax M2.0"
    if "deepseek-r1" in lower or "deepseek r1" in lower:
        return "DeepSeek R1"
    if "deepseek-v3" in lower or "deepseek v3" in lower:
        return "DeepSeek V3"
    if "deepseek-v4" in lower or "deepseek v4" in lower:
        return "DeepSeek V4"
    if lower.startswith("deepseek/"):
        return short_model_name(raw)
    if lower in {"qwq", "qwq-32b"}:
        return "QwQ"
    if lower.startswith("qwq-"):
        return "QwQ"
    if "/" in raw:
        return short_model_name(raw)
    return raw


def teacher_components(raw: str) -> list[str]:
    raw = (raw or "").strip()
    if not raw:
        return ["Unknown teacher"]
    try:
        parsed = json.loads(raw)
    except Exception:
        return [normalize_teacher_name(raw)]
    if isinstance(parsed, list):
        components = [normalize_teacher_name(str(item)) for item in parsed if str(item).strip()]
        return components or ["Unknown teacher"]
    return [normalize_teacher_name(raw)]


def add_weighted_components(
    totals: dict[str, int],
    counts: dict[str, int],
    total_tokens: int,
    components: list[str],
) -> None:
    if not components:
        totals["Unknown teacher"] += total_tokens
        counts["Unknown teacher"] += 1
        return
    component_counts: dict[str, int] = defaultdict(int)
    for component in components:
        component_counts[component] += 1
    remaining = total_tokens
    items = sorted(component_counts.items())
    for idx, (component, count) in enumerate(items):
        if idx == len(items) - 1:
            value = remaining
        else:
            value = round(total_tokens * count / len(components))
            remaining -= value
        totals[component] += value
        counts[component] += 1


def normalized_teacher(row: dict[str, str]) -> str:
    return normalize_teacher_name(row.get("teacher_model", ""))


def normalized_group(row: dict[str, str], group_column: str) -> str:
    if group_column == "teacher_model":
        return normalized_teacher(row)
    return (row.get(group_column, "") or "").strip() or "unknown"


def reasoning_category(row: dict[str, str]) -> str:
    raw = (row.get("reasoning", "") or "").strip()
    lower = raw.lower()
    if lower == "true":
        return "Reasoning"
    if lower == "false" or not lower:
        return "Non-reasoning"
    try:
        parsed = json.loads(lower)
    except Exception:
        return "Reasoning" if "true" in lower else "Non-reasoning"
    if isinstance(parsed, list):
        values = [bool(value) for value in parsed]
        if values and all(values):
            return "Reasoning"
        if not any(values):
            return "Non-reasoning"
        return "Mixed reasoning flags"
    return "Reasoning" if bool(parsed) else "Non-reasoning"


def row_key(row: dict[str, str]) -> str:
    return "\t".join([row.get("dataset_name", ""), row.get("hf_split", ""), row.get("is_agent", "")])


def load_mixed_apportionment() -> dict[str, dict[str, object]]:
    if not MIXED_SAMPLE_JSON.exists():
        return {}
    data = json.loads(MIXED_SAMPLE_JSON.read_text())
    return {row_key(result): result for result in data.get("results", [])}


def aggregate_group(
    rows: list[dict[str, str]],
    group_column: str,
    apportionment: dict[str, dict[str, object]] | None = None,
) -> list[tuple[str, str, int, int]]:
    totals: dict[str, int] = defaultdict(int)
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        if group_column == "teacher_model":
            sample = (apportionment or {}).get(row_key(row))
            if sample and sample.get("status") == "sampled":
                for teacher in sample.get("teachers", []):
                    teacher_name = normalize_teacher_name(str(teacher.get("teacher", "")))
                    totals[teacher_name] += int(teacher.get("estimated_row_tokens") or 0)
                    counts[teacher_name] += 1
                continue
            add_weighted_components(totals, counts, token_count(row), teacher_components(row.get("teacher_model", "")))
            continue
        group = normalized_group(row, group_column)
        totals[group] += token_count(row)
        counts[group] += 1
    return sorted(
        ((group, display_label(group, "unknown"), totals[group], counts[group]) for group in totals),
        key=lambda item: item[2],
        reverse=True,
    )


def reasoning_totals(
    rows: list[dict[str, str]],
    apportionment: dict[str, dict[str, object]],
) -> dict[str, dict[str, int]]:
    totals: dict[str, dict[str, int]] = {
        "Agentic": defaultdict(int),
        "Non-agentic": defaultdict(int),
    }
    for row in rows:
        label = agent_label(row)
        category = reasoning_category(row)
        sample = apportionment.get(row_key(row))
        if category == "Mixed reasoning flags" and sample and sample.get("status") == "sampled":
            totals[label]["Reasoning"] += int(sample.get("estimated_reasoning_tokens") or 0)
            totals[label]["Non-reasoning"] += int(sample.get("estimated_nonreasoning_tokens") or 0)
        elif category == "Mixed reasoning flags":
            totals[label]["Unresolved mixed"] += token_count(row)
        else:
            totals[label][category] += token_count(row)
    return totals


def svg_text(text: str, x: float, y: float, **attrs: str | int | float) -> str:
    attr_text = " ".join(f'{key.replace("_", "-")}="{html.escape(str(value))}"' for key, value in attrs.items())
    return f'<text x="{x:.1f}" y="{y:.1f}" {attr_text}>{html.escape(text)}</text>'


def panel_title(parts: list[str], title: str, subtitle: str, x: float, y: float) -> None:
    parts.append(svg_text(title, x, y, fill="#172026", font_family="Arial, sans-serif", font_size=17, font_weight=700))
    parts.append(svg_text(subtitle, x, y + 20, fill="#4b5563", font_family="Arial, sans-serif", font_size=11))


def render_bar_panel(
    parts: list[str],
    x: float,
    y: float,
    width: float,
    title: str,
    groups: list[tuple[str, str, int, int]],
    total: int,
    color: str,
) -> float:
    row_h = 24
    header_h = 58
    footer_h = 20
    label_w = 320
    value_w = 146
    bar_x = x + label_w
    value_x = x + width - value_w
    bar_w = max(160, value_x - bar_x - 24)
    max_value = max((value for _, _, value, _ in groups), default=1)
    panel_h = header_h + len(groups) * row_h + footer_h

    parts.append(f'<rect x="{x - 14:.1f}" y="{y - 28:.1f}" width="{width + 28:.1f}" height="{panel_h + 40:.1f}" rx="8" fill="#ffffff" stroke="#d1d5db"/>')
    panel_title(
        parts,
        title,
        f"{len(groups)} groups, {compact_tokens(total)} total; linear bars scaled to {compact_tokens(max_value)}",
        x,
        y,
    )
    parts.append(svg_text("Group", x, y + 43, fill="#6b7280", font_family="Arial, sans-serif", font_size=10, font_weight=700))
    parts.append(svg_text("Linear token amount", bar_x, y + 43, fill="#6b7280", font_family="Arial, sans-serif", font_size=10, font_weight=700))
    parts.append(svg_text("Tokens / share", value_x, y + 43, fill="#6b7280", font_family="Arial, sans-serif", font_size=10, font_weight=700))

    for idx, (_, label, value, count) in enumerate(groups):
        row_y = y + header_h + idx * row_h
        if idx % 2 == 0:
            parts.append(f'<rect x="{x - 8:.1f}" y="{row_y - 15:.1f}" width="{width + 16:.1f}" height="{row_h}" fill="#f9fafb"/>')
        parts.append(svg_text(trunc(label, 38), x, row_y, fill="#111827", font_family="Arial, sans-serif", font_size=11))
        bar_width = 0 if max_value <= 0 else bar_w * value / max_value
        if value > 0:
            bar_width = max(1.5, bar_width)
        parts.append(f'<rect x="{bar_x:.1f}" y="{row_y - 12:.1f}" width="{bar_width:.1f}" height="13" rx="2" fill="{color}"/>')
        parts.append(svg_text(f"{compact_tokens(value)} / {percent(value, total)}", value_x, row_y, fill="#111827", font_family="Arial, sans-serif", font_size=11))

    return panel_h + 40


def render_reasoning_panel(
    parts: list[str],
    x: float,
    y: float,
    width: float,
    rows: list[dict[str, str]],
    apportionment: dict[str, dict[str, object]],
) -> float:
    panel_h = 288
    label_w = 130
    bar_x = x + label_w
    bar_w = width - label_w - 20
    category_totals = reasoning_totals(rows, apportionment)
    categories = [
        (category, color)
        for category, color in REASONING_CATEGORIES
        if any(category_totals[label].get(category, 0) > 0 for label in ("Agentic", "Non-agentic"))
    ]

    parts.append(f'<rect x="{x - 14:.1f}" y="{y - 28:.1f}" width="{width + 28:.1f}" height="{panel_h + 40:.1f}" rx="8" fill="#ffffff" stroke="#d1d5db"/>')
    panel_title(parts, "Reasoning vs Non-Reasoning", "Sampled mixed rows are apportioned; unresolved means split files were missing locally", x, y)

    for legend_idx, (category, color) in enumerate(categories):
        lx = x + 300 + legend_idx * 190
        parts.append(f'<rect x="{lx:.1f}" y="{y + 29:.1f}" width="12" height="12" rx="2" fill="{color}"/>')
        parts.append(svg_text(category, lx + 17, y + 40, fill="#374151", font_family="Arial, sans-serif", font_size=11))

    for idx, label in enumerate(("Agentic", "Non-agentic")):
        row_y = y + 75 + idx * 92
        label_total = sum(category_totals[label].values())
        parts.append(svg_text(label, x, row_y + 23, fill="#111827", font_family="Arial, sans-serif", font_size=14, font_weight=700))
        parts.append(svg_text(compact_tokens(label_total), x, row_y + 42, fill="#4b5563", font_family="Arial, sans-serif", font_size=11))
        parts.append(f'<rect x="{bar_x:.1f}" y="{row_y:.1f}" width="{bar_w:.1f}" height="30" rx="4" fill="#f3f4f6"/>')
        cursor = bar_x
        for category, color in categories:
            value = category_totals[label].get(category, 0)
            if value <= 0 or label_total <= 0:
                continue
            segment_w = bar_w * value / label_total
            parts.append(f'<rect x="{cursor:.1f}" y="{row_y:.1f}" width="{segment_w:.1f}" height="30" fill="{color}"/>')
            cursor += segment_w
        for cat_idx, (category, color) in enumerate(categories):
            value = category_totals[label].get(category, 0)
            tx = bar_x + cat_idx * (bar_w / max(1, len(categories)))
            parts.append(svg_text(f"{compact_tokens(value)} ({percent(value, label_total)})", tx, row_y + 53, fill="#111827", font_family="Arial, sans-serif", font_size=10))

    parts.append(
        svg_text(
            "Sample estimates are saved in figures/mixed_reasoning_sample_estimates.{csv,json}.",
            x,
            y + panel_h - 6,
            fill="#6b7280",
            font_family="Arial, sans-serif",
            font_size=10,
        )
    )
    return panel_h + 40


def render_overview(rows: list[dict[str, str]]) -> str:
    width = 2200
    margin = 36
    gap = 42
    inner_w = width - 2 * margin
    col_w = (inner_w - gap) / 2

    agent_rows = [row for row in rows if row.get("is_agent") == "true"]
    non_agent_rows = [row for row in rows if row.get("is_agent") == "false"]
    apportionment = load_mixed_apportionment()
    total = sum(token_count(row) for row in rows)
    agent_total = sum(token_count(row) for row in agent_rows)
    non_agent_total = sum(token_count(row) for row in non_agent_rows)

    agent_teacher = aggregate_group(agent_rows, "teacher_model", apportionment)
    non_agent_teacher = aggregate_group(non_agent_rows, "teacher_model", apportionment)
    agent_harness = aggregate_group(agent_rows, "agent_harness")
    unresolved_mixed = sum(
        token_count(row)
        for row in rows
        if reasoning_category(row) == "Mixed reasoning flags"
        and (not apportionment.get(row_key(row)) or apportionment[row_key(row)].get("status") != "sampled")
    )

    header_h = 150
    top_y = header_h
    teacher_left_h = 58 + len(agent_teacher) * 24 + 60
    teacher_right_h = 58 + len(non_agent_teacher) * 24 + 60
    row_1_h = max(teacher_left_h, teacher_right_h)
    mid_y = top_y + row_1_h + 44
    row_2_h = 328
    height = mid_y + row_2_h + 76

    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<title>SFT Token Overview</title>",
        f"<desc>Combined token overview using avg_estimated_tokens from {html.escape(str(TABLE))}. Bars are linear scale.</desc>",
        '<rect width="100%" height="100%" fill="#f3f4f6"/>',
        svg_text("Code-SWE Terminal SFT Token Overview", margin, 48, fill="#111827", font_family="Arial, sans-serif", font_size=30, font_weight=700),
        svg_text(
            f"{len(rows)} rows under the agentic/non-agentic SFT roots, total avg_estimated_tokens = {compact_tokens(total)} ({total:,}). Bars use linear scale.",
            margin,
            78,
            fill="#4b5563",
            font_family="Arial, sans-serif",
            font_size=14,
        ),
        svg_text(
            f"Mixed reasoning rows are apportioned from local samples where possible; unresolved mixed = {compact_tokens(unresolved_mixed)}.",
            margin,
            98,
            fill="#4b5563",
            font_family="Arial, sans-serif",
            font_size=13,
        ),
    ]

    card_y = 112
    cards = (
        ("All SFT", len(rows), total, "#111827"),
        ("Agentic", len(agent_rows), agent_total, "#2f6f73"),
        ("Non-agentic", len(non_agent_rows), non_agent_total, "#6a4c93"),
    )
    for idx, (label, count, tokens, color) in enumerate(cards):
        x = margin + idx * 246
        parts.append(f'<rect x="{x:.1f}" y="{card_y:.1f}" width="216" height="48" rx="8" fill="#ffffff" stroke="#d1d5db"/>')
        parts.append(svg_text(label, x + 14, card_y + 19, fill="#4b5563", font_family="Arial, sans-serif", font_size=11, font_weight=700))
        parts.append(svg_text(f"{compact_tokens(tokens)}", x + 14, card_y + 39, fill=color, font_family="Arial, sans-serif", font_size=19, font_weight=700))
        parts.append(svg_text(f"{count} rows", x + 125, card_y + 39, fill="#6b7280", font_family="Arial, sans-serif", font_size=11))

    render_bar_panel(parts, margin, top_y + 32, col_w, "Agentic Tokens by Teacher", agent_teacher, agent_total, "#2f6f73")
    render_bar_panel(parts, margin + col_w + gap, top_y + 32, col_w, "Non-Agentic Tokens by Teacher", non_agent_teacher, non_agent_total, "#6a4c93")
    render_bar_panel(parts, margin, mid_y + 32, col_w, "Agentic Tokens by Harness", agent_harness, agent_total, "#b45f33")
    render_reasoning_panel(parts, margin + col_w + gap, mid_y + 32, col_w, rows, apportionment)

    parts.append(
        svg_text(
            "Source: split_datasets.csv plus mixed_reasoning_sample_estimates.json. Teacher lists are split across listed teachers; DeepSeek R1/V3 variants and Claude/Opus variants are grouped.",
            margin,
            height - 24,
            fill="#6b7280",
            font_family="Arial, sans-serif",
            font_size=11,
        )
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    if not rows:
        raise RuntimeError("no SFT rows with token estimates found")
    OUTPUT.write_text(render_overview(rows))
    for name in OBSOLETE_FIGURES:
        path = OUT_DIR / name
        if path.exists():
            path.unlink()
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
