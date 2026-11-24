"""Make the Judge Smile — entry writer (v2).

Writes one line, at most 200 characters, about a small good thing that
happened today, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt
for local runs). Python 3.13 standard library only, deterministic, no
network access. A self-check enforces the competition gate before the
file is written: UTF-8 text, 1 to 200 characters, not only whitespace,
single line.

Chosen line (see CANDIDATES.md): a kid in yellow boots fishes the
narrator's keys out of a puddle with a stick, then charges exactly one
high-five — warmth, a surprise turn in the ending, four concrete small
details, fresh wording.
"""

import os
import sys

MAX_CHARS = 200

ENTRY_LINES = [
    "I dropped my keys in a puddle this morning, and a kid in yellow "
    "boots fished them out with a stick \u2014 then charged me exactly "
    "one high-five.",
]

ENTRY = "".join(ENTRY_LINES)


def gate_problems(text):
    """Return the list of gate violations (empty when the entry is valid)."""
    problems = []
    if not text:
        problems.append("entry is empty")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if text.strip() == "":
        problems.append("entry is only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not encodable as UTF-8")
    return problems


def write_entry(out_dir, text):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def main():
    problems = gate_problems(ENTRY)
    if problems:
        for problem in problems:
            print("gate failed: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(out_dir, ENTRY)
    print("wrote %s (%d characters)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
