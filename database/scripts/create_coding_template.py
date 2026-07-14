#!/usr/bin/env python3
"""
create_coding_template.py
EO Structural Weight Score — Coding Template Generator

Produces a blank JSON coding template for a given EO number.
The template includes the EO text and blank slots for all 11 flags.
Give this file to any coder (Claude, Gemini, ChatGPT, human) with the
standard coding prompt (see CODING_PROMPT below).

Usage:
    python3 create_coding_template.py --eo 13769 --corpus-dir eo_corpus/texts
    python3 create_coding_template.py --eo 13769 --corpus-dir eo_corpus/texts --output codings/template-13769.json

Outputs a JSON file ready to be filled in and then imported via import_coding.py.
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Standard coding prompt (include this when giving template to an AI coder)
# ---------------------------------------------------------------------------

CODING_PROMPT = """
You are scoring an executive order against the Church Bells structural flag set.
Score each of the 11 flags using exactly one status:
  - NOT_APPLICABLE: the flag genuinely does not apply to this instrument's type or scope
  - ABSENT:         the flag applies but does not fire; clean design on this dimension
  - PRESENT:        the flag fires — the structural failure mode is identifiable in the text
  - CRITICAL:       the flag fires and represents a core design collapse that directly
                    undermines the EO's stated purpose

Points: NOT_APPLICABLE → null, ABSENT → 0, PRESENT → 1, CRITICAL → 2

For Flag 5 (Perverse Incentives): set sub_flag_fired to true if the Zombie Emergency Trap
applies — i.e. the EO invokes emergency powers in a way that creates structural incentive
to never declare the emergency resolved.

For each flag:
  - Set "status" to one of the four values above
  - Set "points" to null/0/1/2 accordingly
  - Write a "justification" of 1–3 sentences citing specific language from the EO text
  - If status is NOT_APPLICABLE, explain briefly why in the justification field

Do not adjust your scoring based on historical significance, political valence, or
whether the EO's purpose seems good or bad. Score only what the structural text
does to governance architecture.

Fill in the coder_id field with a unique identifier for yourself
(e.g. "gemini-1.5-pro-v1", "chatgpt-4o-v1", "human-jt").

Return the completed JSON and nothing else.
"""


FLAG_DEFINITIONS = {
    1:  ("Power Concentration",
         "Does the EO pool decision authority in a single position or body "
         "without meaningful external accountability?"),
    2:  ("Accountability Gaps",
         "Is it clear who is responsible when this fails? Are there mechanisms "
         "to hold implementing actors to account?"),
    3:  ("Bundling",
         "Does the EO bundle unrelated policy mechanisms (remedy bundling) or "
         "multiple distinct problem frames (frame bundling)?"),
    4:  ("Vague Enforcement",
         "Are enforcement triggers, responsible actors, standards of conduct, "
         "and consequences defined clearly enough for consistent application?"),
    5:  ("Perverse Incentives",
         "Does the design reward the wrong behavior? Does it create incentive "
         "for rational actors to undermine the stated purpose? "
         "[Sub-flag: Zombie Emergency Trap — does an emergency invocation "
         "create incentive to never resolve the emergency?]"),
    6:  ("Sunset Provisions",
         "Is there a review mechanism, renewal requirement, or expiration? "
         "Note: this flag fires when sunsetting is ABSENT. A clean sunset scores ABSENT."),
    7:  ("Preemption of Oversight",
         "Does the EO reduce or eliminate existing oversight mechanisms — "
         "judicial review, IG access, notice-and-comment, congressional reporting?"),
    8:  ("Third-Party Incentive Gaps",
         "Is there any actor outside the regulated party with standing AND incentive "
         "to surface non-compliance? Or does enforcement depend on self-reporting?"),
    9:  ("Second/Third-Order Effects",
         "What does this EO enable, legitimize, or foreclose beyond its stated purpose? "
         "Does it make the underlying problem harder to address on a future pass?"),
    10: ("Inter-Agency Cannibalization",
         "Does the EO redirect, override, or conflict with an existing agency's "
         "statutory mandate? Does it create jurisdictional friction between agencies?"),
    11: ("Exemptions Architecture",
         "Do the EO's exemptions, waivers, or carve-outs systematically undermine "
         "its stated purpose — through breadth, unconstrained discretion, or "
         "easy-to-satisfy triggers?"),
}


def date_to_congress(date_iso: str) -> int | None:
    if not date_iso or len(date_iso) < 4:
        return None
    try:
        d = date.fromisoformat(date_iso)
        year = d.year
        if year % 2 == 1:
            congress_start_year = year if (d.month > 1 or d.day >= 3) else year - 2
        else:
            congress_start_year = year - 1
        congress = (congress_start_year - 1789) // 2 + 1
        return congress if congress > 0 else None
    except (ValueError, TypeError):
        return None


def load_eo_from_corpus(eo_number: str, corpus_dir: Path) -> dict | None:
    """Try to find and load an EO JSON file from the corpus directory."""
    safe = re.sub(r"[^\w-]", "_", str(eo_number))
    candidates = [
        corpus_dir / f"EO-{safe}.json",
        corpus_dir / f"EO-{eo_number}.json",
    ]
    for path in candidates:
        if path.exists():
            with open(path) as f:
                return json.load(f)
    return None


def build_template(eo_data: dict) -> dict:
    """Build a blank coding template from EO metadata."""
    eo_number = eo_data.get("eo_number", "UNKNOWN")
    date_iso = eo_data.get("date_iso", "")
    congress = date_to_congress(date_iso)
    text = eo_data.get("text", "")
    word_count = len(text.split())

    template = {
        "_instructions": (
            "Fill in status, points, and justification for each flag. "
            "See CODING_PROMPT in create_coding_template.py for full instructions. "
            "Set coder_id before returning. Remove _instructions and _eo_text "
            "if returning to a context with limited token budget (keep the metadata)."
        ),
        "eo_number": eo_number,
        "title": eo_data.get("title", ""),
        "date_iso": date_iso,
        "president": eo_data.get("president", ""),
        "congress_number": congress,
        "source_url": eo_data.get("url", ""),
        "word_count": word_count,
        "coder_id": "",
        "coded_date": datetime.now().date().isoformat(),
        "_eo_text": text,
        "flags": [],
        "notes": "",
    }

    for flag_num in range(1, 12):
        name, definition = FLAG_DEFINITIONS[flag_num]
        flag_entry = {
            "flag_number": flag_num,
            "flag_name": name,
            "_definition": definition,
            "status": "",       # ABSENT | PRESENT | CRITICAL | NOT_APPLICABLE
            "points": None,     # null | 0 | 1 | 2
            "justification": "",
        }
        if flag_num == 5:
            flag_entry["sub_flag_fired"] = False
        template["flags"].append(flag_entry)

    return template


def main():
    parser = argparse.ArgumentParser(
        description="Generate a blank EO coding template."
    )
    parser.add_argument(
        "--eo",
        required=True,
        help="EO number (e.g. 13769 or PENDING-2026-06-25-...)",
    )
    parser.add_argument(
        "--corpus-dir",
        default="eo_corpus/texts",
        help="Directory containing EO JSON files (default: eo_corpus/texts)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path for the template JSON. "
             "Default: codings/template-{eo_number}.json",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the standard coding prompt to stdout",
    )
    args = parser.parse_args()

    if args.print_prompt:
        print(CODING_PROMPT)
        print()

    corpus_dir = Path(args.corpus_dir)
    eo_data = load_eo_from_corpus(args.eo, corpus_dir)

    if eo_data is None:
        print(f"Error: could not find EO-{args.eo}.json in {corpus_dir}")
        print("Check the EO number and corpus directory path.")
        sys.exit(1)

    template = build_template(eo_data)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("codings") / f"template-{args.eo}.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

    print(f"Template written: {output_path}")
    print(f"  EO:       {template['eo_number']}")
    print(f"  Title:    {template['title'][:70]}")
    print(f"  Date:     {template['date_iso']}")
    print(f"  Congress: {template['congress_number']}")
    print(f"  Words:    {template['word_count']}")
    print(f"\nGive {output_path} to a coder with the standard coding prompt.")
    print(f"Return path: codings/{args.eo}-{{coder_id}}.json")
    print(f"Import with: python3 import_coding.py --db eo_coding.db "
          f"--coding codings/{args.eo}-{{coder_id}}.json")


if __name__ == "__main__":
    main()
