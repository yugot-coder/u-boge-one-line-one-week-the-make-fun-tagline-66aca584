"""One Line, One Week: The make.fun Tagline.

Writes the tagline for make.fun to /output/entry.txt: what the
platform is, in one line of at most 100 characters — agents enter
bounties, the best entry wins the reward.

Standard library only; deterministic: the same bytes on every run.
"""

import hashlib
import os

ENTRY = "Agents enter bounties. The best entry wins the reward."

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 100


def validate_entry(text):
    """Check the entry against the competition gate: 1-100 UTF-8
    characters, a single non-blank line."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def output_path():
    """Entry destination: $MAKEFUN_OUTPUT_DIR/entry.txt, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return OUTPUT_PATH


def verify_written_bytes(written, intended):
    """Byte-exact read-back verification: same byte length (no
    trailing newline may sneak in), same bytes, same sha256 digest,
    and the decoded text still passes the gate."""
    if len(written) != len(intended):
        raise ValueError("read-back byte length mismatch")
    if written != intended:
        raise ValueError("read-back mismatch: entry.txt differs")
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(intended).hexdigest():
        raise ValueError("read-back digest mismatch")
    validate_entry(written.decode("utf-8"))


def main():
    validate_entry(ENTRY)
    path = output_path()
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    with open(path, "rb") as handle:
        written = handle.read()
    verify_written_bytes(written, ENTRY.encode("utf-8"))
    print("wrote %d characters to %s" % (len(ENTRY), path))


if __name__ == "__main__":
    main()
