#!/usr/bin/env python3
"""
password_generator.py

Generates cryptographically secure random passwords using Python's
`secrets` module (not `random`, which is not safe for secrets).

Usage:
    python password_generator.py [length] [count] [options]

Options:
    --no-symbols     Exclude symbols (!@#$%^&* etc.)
    --no-digits      Exclude digits
    --no-upper       Exclude uppercase letters
    --no-lower       Exclude lowercase letters
    --no-ambiguous   Exclude ambiguous characters (l, 1, I, O, 0, etc.)

Examples:
    python password_generator.py                # one 16-char password
    python password_generator.py 20 5            # five 20-char passwords
    python password_generator.py 12 1 --no-symbols
"""

import sys
import string
import secrets

AMBIGUOUS = "l1IO0"


def build_charset(no_symbols, no_digits, no_upper, no_lower, no_ambiguous):
    charset = ""
    if not no_lower:
        charset += string.ascii_lowercase
    if not no_upper:
        charset += string.ascii_uppercase
    if not no_digits:
        charset += string.digits
    if not no_symbols:
        charset += "!@#$%^&*()-_=+[]{};:,.<>?/"

    if no_ambiguous:
        charset = "".join(c for c in charset if c not in AMBIGUOUS)

    if not charset:
        print("[!] All character sets excluded — nothing to generate from.")
        sys.exit(1)

    return charset


def generate_password(length: int, charset: str) -> str:
    return "".join(secrets.choice(charset) for _ in range(length))


def main():
    args = sys.argv[1:]
    flags = {a for a in args if a.startswith("--")}
    positional = [a for a in args if not a.startswith("--")]

    length = int(positional[0]) if len(positional) >= 1 else 16
    count = int(positional[1]) if len(positional) >= 2 else 1

    if length < 4:
        print("[!] Length should be at least 4 for a meaningful password.")
        sys.exit(1)

    charset = build_charset(
        no_symbols="--no-symbols" in flags,
        no_digits="--no-digits" in flags,
        no_upper="--no-upper" in flags,
        no_lower="--no-lower" in flags,
        no_ambiguous="--no-ambiguous" in flags,
    )

    print(f"[*] Generating {count} password(s) of length {length}:\n")
    for _ in range(count):
        print(generate_password(length, charset))


if __name__ == "__main__":
    main()
