#!/usr/bin/env python3
"""The joke about the demo.

Writes one line of text to /output/entry.txt: a joke about working
beside an AI coding agent, told the way it happens in every demo —
the agent swears everything is ready, and the demo falls over the
moment the narrator clicks the button labelled Demo.

The program is deliberately boring on purpose: the joke is the
deliverable, and the code exists only to carry it to the output file
exactly as written, then prove it got there unchanged.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import sys

# The entry: one line, written fresh in this session. The setup is the
# agent's confidence ("swore the demo was ready"); the turn is that the
# crash happens live, in front of the room, the moment the narrator
# clicks; the punchline is the label on that button — Demo — which the
# reader has to connect themselves, no explanation given.
JOKE = (
    "My agent swore the demo was ready, then it crashed the moment I "
    "clicked Demo."
)

# The competition's gate: 1 to 280 Unicode code points, and the text
# must not be only white space.
MIN_CHARS = 1
MAX_CHARS = 280


def resolve_output_dir() -> str:
    """Where the entry goes: the harness's override, else /output."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if override:
        return override
    return "/output"


def check_joke(text: str) -> None:
    """Fail loudly if the joke breaks the gate, so a bad entry is
    never written silently."""
    if not isinstance(text, str):
        raise TypeError("joke must be text, got %r" % type(text).__name__)
    length = len(text)
    if length < MIN_CHARS or length > MAX_CHARS:
        raise ValueError(
            "joke is %d code points, gate is %d-%d"
            % (length, MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("joke must not be only white space")
    if "\n" in text.strip("\n") or "\r" in text:
        # One line: no line breaks inside the joke itself.
        raise ValueError("joke must be a single line")


def main() -> int:
    check_joke(JOKE)

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(JOKE)

    # Read it back and prove the bytes on disk are exactly the joke.
    with open(out_path, "r", encoding="utf-8") as fh:
        on_disk = fh.read()
    if on_disk != JOKE:
        raise RuntimeError("entry on disk does not match the joke")

    print("wrote %s: %d characters" % (out_path, len(JOKE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
