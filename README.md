# sys-utils

A small collection of standalone Python utility scripts for everyday
system tasks. Each script works independently no shared code, just
copy the ones you need.

## Scripts included

| Script                  | What it does                                                        |
|--------------------------|----------------------------------------------------------------------|
| `file_organizer.py`      | Sorts files in a folder into subfolders by type (Images, Documents, etc.) |
| `password_generator.py`  | Generates cryptographically secure random passwords                 |
| `disk_checker.py`        | Reports disk usage per partition and warns on low free space         |
| `duplicate_finder.py`    | Finds (and optionally deletes) duplicate files by content, not name  |
| `system_info.py`         | Prints a quick OS / CPU / memory / disk / battery snapshot           |

## Requirements

- Python 3.7+
- Some scripts use [`psutil`](https://pypi.org/project/psutil/) for
  hardware info:

```bash
pip install psutil
```

`file_organizer.py`, `password_generator.py`, and `duplicate_finder.py`
use only the Python standard library — no extra installs needed.

---

## 1. `file_organizer.py`

Moves files into subfolders (`Images/`, `Documents/`, `Audio/`, etc.)
based on their extension.

```bash
python file_organizer.py ~/Downloads
python file_organizer.py ~/Downloads --dry-run   # preview only
```

Files with unrecognized extensions go into an `Other/` folder. Existing
files with the same name are auto-renamed (`file_1.txt`) rather than
overwritten.

## 2. `password_generator.py`

Generates secure random passwords using Python's `secrets` module.

```bash
python password_generator.py                # one 16-character password
python password_generator.py 20 5            # five 20-character passwords
python password_generator.py 12 1 --no-symbols --no-ambiguous
```

Flags: `--no-symbols`, `--no-digits`, `--no-upper`, `--no-lower`,
`--no-ambiguous` (excludes look-alike characters like `l`, `1`, `I`, `O`, `0`).

## 3. `disk_checker.py`

Reports usage for all mounted partitions, or specific paths, and flags
any that exceed a usage threshold.

```bash
python disk_checker.py                       # all partitions, warn at 90%
python disk_checker.py / /home                # specific paths
python disk_checker.py --threshold 80         # custom warning threshold
```

Requires `psutil` only when auto-detecting all partitions — checking
specific paths works without it.

## 4. `duplicate_finder.py`

Recursively scans a directory and groups files that have identical
content (via SHA-256 hash), regardless of filename.

```bash
python duplicate_finder.py ~/Downloads
python duplicate_finder.py ~/Downloads --delete   # deletes all but first copy of each set
```

**Always run without `--delete` first** to review what will be removed.

## 5. `system_info.py`

Prints a snapshot of OS, CPU, memory, disk, and battery info.

```bash
python system_info.py
```

---

## Notes

- All scripts are read-only/inspection tools by default except
  `file_organizer.py` (moves files) and `duplicate_finder.py --delete`
  (deletes files) — both support a safe preview/dry-run first.
- Tested with standard library + `psutil`; no other third-party
  dependencies.
