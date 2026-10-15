"""Render article milestones from retained research; Python standard library only.

Run from any directory: python week3/images/render_timeline.py
Dates are spaced proportionally in UTC. This selects episodes, not every origin.
"""

import csv
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START, END = date(2022, 12, 1), date(2026, 10, 1)
NAVY, BLUE, PURPLE, GRAY = "#17243C", "#2667DA", "#6953BD", "#CCD3DF"

# Project/date/kind keys match the existing chronology. All labels are editorial.
EVENTS = [
    ("Jupytee", "2022-12-20", "implementation", 45, "above",
     "Jupytee experiment", ["Model prompts through", "notebook commands"]),
    ("Jupyter AI", "2023-08-02", "release_announcement", 140, "below",
     "Jupyter AI launches", ["Chat and magics;", "a choice of models"]),
    ("JupyterLite AI", "2024-06-10", "implementation", 350, "above",
     "Codestral experiment", ["Completion and chat;", "later JupyterLite AI"]),
    ("Jupyter AI", "2025-10-28", "announcement", 680, "below",
     "Split announced", ["Existing code organized", "into focused packages"]),
    ("Jupyter AI", "2026-04-01", "published_release", 810, "above",
     "Jupyter AI 3.0", ["External agents;", "notebook tools"]),
    ("Jupyter AI", "2026-09-03", "published_release", 910, "below",
     "Jupyter AI 3.2", ["Shared commands;", "JSD optional"]),
]


def x_at(day):
    return 70 + (day - START).days / (END - START).days * 960


def text(x, y, value, size=22, weight="400", color=NAVY, anchor="start"):
    return (f'<text x="{x:.2f}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}">{escape(value)}</text>')


def main():
    with (ROOT / "data/timeline.csv").open(newline="", encoding="utf-8") as source:
        records = list(csv.DictReader(source))
    selected = []
    for project, day, kind, label_x, side, title, lines in EVENTS:
        matches = [r for r in records if (r["project"], r["date"], r["event_kind"])
                   == (project, day, kind)]
        if len(matches) != 1:
            raise ValueError(f"Expected one record for {project}, {day}, {kind}")
        selected.append((matches[0], label_x, side, title, lines))
    descriptions = "; ".join(f'{r["date"]}: {title}, {", ".join(lines)}'
                             for r, _, _, title, lines in selected)
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="585" '
        'viewBox="0 0 1100 585" role="img" aria-labelledby="title desc">',
        '<title id="title">AI around Jupyter: selected milestones</title>',
        f'<desc id="desc">{escape(descriptions)}. Dates are spaced proportionally. '
        'These events do not imply that one technique replaced another.</desc>',
        '<rect width="1100" height="585" fill="#FFFFFF"/>',
        text(45, 55, "AI around Jupyter: selected milestones", 34, "700"),
        text(45, 94, "Experiments, integration and reusable notebook tools", 22),
        f'<line x1="70" x2="1030" y1="300" y2="300" stroke="{GRAY}" stroke-width="3"/>',
    ]
    for year in range(2023, 2027):
        x = x_at(date(year, 1, 1))
        svg += [f'<line x1="{x:.2f}" x2="{x:.2f}" y1="300" y2="310" '
                f'stroke="{GRAY}" stroke-width="2"/>',
                text(x, 335, str(year), 20, anchor="middle")]
    for record, label_x, side, title, lines in selected:
        day = date.fromisoformat(record["date"])
        x = x_at(day)
        top = side == "above"
        end = 260 if top else 365
        ys = [148, 180, 211, 239] if top else [397, 430, 460, 488]
        label = f'{day.day} {day.strftime("%b %Y")}'
        svg += [f'<a href="{escape(record["url"], quote=True)}">',
                f'<title>{escape(record["date"] + ": " + title + "; " + record["event_kind"])}</title>',
                f'<line x1="{x:.2f}" x2="{x:.2f}" y1="300" y2="{end}" '
                f'stroke="{GRAY}" stroke-width="2"/>',
                f'<circle cx="{x:.2f}" cy="300" r="7" fill="{BLUE}"/>',
                text(label_x, ys[0], label, 22, "700", PURPLE),
                text(label_x, ys[1], title, 22, "700"),
                text(label_x, ys[2], lines[0], 20),
                text(label_x, ys[3], lines[1], 20), '</a>']
    svg += [text(45, 538, "Selected events, not a replacement sequence. Earlier completion tools predate this view.", 19),
            text(45, 568, "Dates: UTC. Evidence through October 14, 2026. Sources: week3/data/timeline.csv.", 19),
            '</svg>']
    (ROOT / "images/ai-timeline.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
