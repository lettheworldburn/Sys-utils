#!/usr/bin/env python3
"""
disk_checker.py

Checks disk usage for one or more paths (or all mounted partitions by
default) and warns when free space drops below a threshold.

Requires:
    pip install psutil

Usage:
    python disk_checker.py [path1 path2 ...] [--threshold PERCENT]

Examples:
    python disk_checker.py                     # check all partitions, warn at 90%
    python disk_checker.py / /home              # check specific paths
    python disk_checker.py --threshold 80        # custom warning threshold
"""

import sys
import shutil

try:
    import psutil
except ImportError:
    psutil = None


def human_readable(num_bytes: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f}{unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f}EB"


def check_path(path: str, threshold: float):
    try:
        usage = shutil.disk_usage(path)
    except FileNotFoundError:
        print(f"[!] Path not found: {path}")
        return

    percent_used = usage.used / usage.total * 100
    status = "⚠️  LOW SPACE" if percent_used >= threshold else "OK"

    print(f"\nPath: {path}")
    print(f"  Total: {human_readable(usage.total)}")
    print(f"  Used:  {human_readable(usage.used)} ({percent_used:.1f}%)")
    print(f"  Free:  {human_readable(usage.free)}")
    print(f"  Status: {status}")


def get_all_partitions():
    if psutil is None:
        print(
            "[!] psutil not installed — cannot auto-detect all partitions.\n"
            "    Install it with `pip install psutil`, or pass specific paths\n"
            "    as arguments instead (e.g. `python disk_checker.py /`)."
        )
        sys.exit(1)
    return [p.mountpoint for p in psutil.disk_partitions(all=False)]


def main():
    args = sys.argv[1:]
    threshold = 90.0

    if "--threshold" in args:
        idx = args.index("--threshold")
        threshold = float(args[idx + 1])
        del args[idx : idx + 2]

    paths = args if args else get_all_partitions()

    print(f"[*] Checking disk usage (warning threshold: {threshold}%)")
    for path in paths:
        check_path(path, threshold)


if __name__ == "__main__":
    main()
