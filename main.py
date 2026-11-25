#!/usr/bin/env python3
"""Write the competition entry to /output/entry.txt.

The entry is one passive-aggressive note a smart fridge leaves for its
owner. The text lives in entry.txt next to this script; this runner
copies it byte-for-byte to the output directory, so the judged text is
exactly the text in this repository.

The runner takes MAKEFUN_OUTPUT_DIR (default /output), creates it if
needed, and writes the entry there as entry.txt (UTF-8, no trailing
newline). Pure standard library only.
"""
import os

ENTRY_FILE = "entry.txt"
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"

# Competition length budget: the gate accepts 1 to 200 characters.
MAX_ENTRY_LENGTH = 200


def load_entry():
    """Read the entry text from entry.txt beside this script.

    A trailing newline in the shipped file is not part of the entry,
    so it is stripped here; the interior of the text is untouched.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, ENTRY_FILE)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().rstrip("\n")


def validate_entry(text):
    """Check the entry against the competition rules; raise on failure.

    Rules: the entry must not be blank, must be exactly one line, and
    must fit within MAX_ENTRY_LENGTH characters.
    """
    if not text or not text.strip():
        raise ValueError("ENTRY must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("ENTRY must be a single line")
    if len(text) > MAX_ENTRY_LENGTH:
        raise ValueError(
            "ENTRY is %d characters, over the %d-character limit"
            % (len(text), MAX_ENTRY_LENGTH)
        )
    return text


def resolve_output_dir():
    """Pick the output directory: env var, or the default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)


def write_entry(output_dir=None):
    """Write the entry to entry.txt in output_dir; return the path."""
    text = validate_entry(load_entry())
    output_dir = output_dir or resolve_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(path, "r", encoding="utf-8") as f:
        actual = f.read()
    if actual != text:
        raise ValueError("entry.txt on disk does not match entry.txt")
    print(text)
    return path


def main():
    write_entry()


if __name__ == "__main__":
    main()
