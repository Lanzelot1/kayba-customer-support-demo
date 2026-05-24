"""Render evidence/skills.md and evidence/external_agent_injection.txt.

The packaged skillbook (`evidence/skillbook.json`) was produced by an
earlier ACE schema (custom section names, fields
`content`/`justification`/`evidence`) and is shipped verbatim because it
is the artefact that produced the headline +20 pp lift on tau2-bench
airline. We render it directly from JSON instead of round-tripping
through `ace.Skillbook` so the on-disk skillbook stays canonical.

Re-run after editing `evidence/skillbook.json`:

    uv run python build_evidence.py
"""

from __future__ import annotations

import json
from pathlib import Path

DEMO = Path(__file__).resolve().parent
SKILLBOOK = DEMO / "evidence" / "skillbook.json"
SKILLS_MD = DEMO / "evidence" / "skills.md"
INJECTION = DEMO / "evidence" / "external_agent_injection.txt"


def _section_title(section: str) -> str:
    return section.replace("_", " ").title()


def render_skills_md(skills_by_section: dict[str, list[dict]]) -> str:
    total = sum(len(v) for v in skills_by_section.values())
    lines = [
        "# Learned skills (skillbook)",
        "",
        f"Distilled by ACE from 30 tau2-bench airline rollouts. "
        f"{total} skills across {len(skills_by_section)} sections. "
        "Each skill carries the agent's failure mode (`content`) and the "
        "evidence that motivated it.",
        "",
    ]
    for section in sorted(skills_by_section):
        skills = skills_by_section[section]
        lines.append(f"## {_section_title(section)} ({len(skills)})")
        lines.append("")
        for s in skills:
            sid = s.get("id", "?")
            content = (s.get("content") or "").strip()
            lines.append(f"- **{sid}** — {content}")
            evidence = (s.get("evidence") or "").strip()
            if evidence:
                evidence_one_line = " ".join(evidence.split())
                if len(evidence_one_line) > 280:
                    evidence_one_line = evidence_one_line[:277] + "..."
                lines.append(f"  - _Evidence:_ {evidence_one_line}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_injection(skills_by_section: dict[str, list[dict]]) -> str:
    """Wrap the skillbook for paste-in to an external agent prompt.

    Mirrors the spirit of `ace.implementations.prompts.
    wrap_skillbook_for_external_agent` without depending on the current
    Skillbook schema.
    """
    body: list[str] = []
    for section in sorted(skills_by_section):
        body.append(f"## {_section_title(section)}")
        for s in skills_by_section[section]:
            content = (s.get("content") or "").strip()
            if content:
                body.append(f"- {content}")
        body.append("")
    body_text = "\n".join(body).rstrip()

    header = (
        "## Strategic Knowledge (Learned from tau2-bench airline rollouts)\n\n"
        "The following strategies were distilled by the ACE Reflector + "
        "SkillManager from 30 multi-turn customer-support conversations. "
        "Apply them when the situation matches; favour explicit, defensible "
        "behaviour over implicit assumptions.\n"
    )
    footer = (
        "\n\nUsage:\n"
        "- Treat each line as a rule the customer-support policy expects.\n"
        "- When multiple rules apply, prefer the one with the most specific "
        "trigger.\n"
        "- These rules supplement (not replace) the domain policy in your "
        "system prompt."
    )
    return header + "\n" + body_text + footer + "\n"


def main() -> None:
    sb = json.loads(SKILLBOOK.read_text())
    skills = sb["skills"]
    items = list(skills.values()) if isinstance(skills, dict) else list(skills)

    by_section: dict[str, list[dict]] = {}
    for s in items:
        if s.get("status") and s["status"] != "active":
            continue
        by_section.setdefault(s.get("section", "uncategorized"), []).append(s)

    for v in by_section.values():
        v.sort(key=lambda s: s.get("id", ""))

    SKILLS_MD.write_text(render_skills_md(by_section))
    INJECTION.write_text(render_injection(by_section))
    print(f"wrote {SKILLS_MD} ({SKILLS_MD.stat().st_size} bytes)")
    print(f"wrote {INJECTION} ({INJECTION.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
