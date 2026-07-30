#!/usr/bin/env python3
"""
file_organizer.py

Organizes files in a directory into subfolders based on their file
extension (e.g. .jpg -> Images/, .pdf -> Documents/).

Usage:
    python file_organizer.py <directory> [--dry-run]

Example:
    python file_organizer.py ~/Downloads
    python file_organizer.py ~/Downloads --dry-run   # preview only, no changes
"""

import sys
import shutil
from pathlib import Path

# Map of extensions -> destination folder name
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".key"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sh"],
    "Executables": [".exe", ".msi", ".dmg", ".app"],
}


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize(directory: Path, dry_run: bool = False):
    if not directory.is_dir():
        print(f"[!] Not a valid directory: {directory}")
        sys.exit(1)

    moved_count = 0

    for item in directory.iterdir():
        # Skip directories and hidden files
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        dest_folder = directory / category
        dest_path = dest_folder / item.name

        if dry_run:
            print(f"[DRY RUN] Would move: {item.name} -> {category}/")
        else:
            dest_folder.mkdir(exist_ok=True)
            # Avoid overwriting existing files with the same name
            if dest_path.exists():
                stem, suffix = item.stem, item.suffix
                counter = 1
                while dest_path.exists():
                    dest_path = dest_folder / f"{stem}_{counter}{suffix}"
                    counter += 1
            shutil.move(str(item), str(dest_path))
            print(f"[+] Moved: {item.name} -> {category}/{dest_path.name}")

        moved_count += 1

    if moved_count == 0:
        print("[*] No files to organize.")
    else:
        action = "Would organize" if dry_run else "Organized"
        print(f"\n[+] {action} {moved_count} file(s).")


def main():
    if len(sys.argv) < 2:
        print("Usage: python file_organizer.py <directory> [--dry-run]")
        sys.exit(1)

    directory = Path(sys.argv[1]).expanduser().resolve()
    dry_run = "--dry-run" in sys.argv[2:]

    organize(directory, dry_run)


if __name__ == "__main__":
    main()
