#!/usr/bin/env python3
"""
duplicate_finder.py

Scans a directory (recursively) for duplicate files based on content
hash (SHA-256), not just filename — so it catches renamed duplicates
too.

Usage:
    python duplicate_finder.py <directory> [--delete]

Options:
    --delete    Delete duplicates, keeping only the first copy found
                (use with caution — review the printed list first!)

Example:
    python duplicate_finder.py ~/Downloads
    python duplicate_finder.py ~/Downloads --delete
"""

import sys
import hashlib
from pathlib import Path
from collections import defaultdict


def hash_file(path: Path, block_size: int = 65536) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(block_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(directory: Path):
    hashes = defaultdict(list)

    for path in directory.rglob("*"):
        if path.is_file():
            try:
                file_hash = hash_file(path)
                hashes[file_hash].append(path)
            except (PermissionError, OSError) as e:
                print(f"[!] Skipping {path}: {e}")

    return {h: paths for h, paths in hashes.items() if len(paths) > 1}


def main():
    if len(sys.argv) < 2:
        print("Usage: python duplicate_finder.py <directory> [--delete]")
        sys.exit(1)

    directory = Path(sys.argv[1]).expanduser().resolve()
    delete_mode = "--delete" in sys.argv[2:]

    if not directory.is_dir():
        print(f"[!] Not a valid directory: {directory}")
        sys.exit(1)

    print(f"[*] Scanning {directory} for duplicates...\n")
    duplicates = find_duplicates(directory)

    if not duplicates:
        print("[+] No duplicates found.")
        return

    total_wasted = 0
    for file_hash, paths in duplicates.items():
        print(f"Duplicate set ({len(paths)} files):")
        for p in paths:
            print(f"  - {p}")

        if delete_mode:
            keep, *remove = paths
            for p in remove:
                size = p.stat().st_size
                p.unlink()
                total_wasted += size
                print(f"  [x] Deleted: {p}")
            print(f"  [+] Kept: {keep}")
        print()

    if delete_mode:
        print(f"[+] Reclaimed {total_wasted / (1024*1024):.2f} MB.")
    else:
        print("[*] Run again with --delete to remove duplicates (keeps first copy of each set).")


if __name__ == "__main__":
    main()
