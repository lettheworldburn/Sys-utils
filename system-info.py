import platform
import sys
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None


def human_readable(num_bytes: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f}{unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f}PB"


def main():
    print("=" * 50)
    print("SYSTEM INFO SNAPSHOT")
    print("=" * 50)
    print(f"Timestamp:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"OS:             {platform.system()} {platform.release()}")
    print(f"OS Version:     {platform.version()}")
    print(f"Machine:        {platform.machine()}")
    print(f"Processor:      {platform.processor() or 'Unknown'}")
    print(f"Python Version: {platform.python_version()}")

    if psutil is None:
        print(
            "\n[!] psutil not installed — skipping CPU/memory/disk details.\n"
            "    Install it with: pip install psutil"
        )
        sys.exit(0)

    print("\n--- CPU ---")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Logical cores:  {psutil.cpu_count(logical=True)}")
    print(f"Current usage:  {psutil.cpu_percent(interval=1)}%")

    print("\n--- Memory ---")
    mem = psutil.virtual_memory()
    print(f"Total:     {human_readable(mem.total)}")
    print(f"Available: {human_readable(mem.available)}")
    print(f"Used:      {human_readable(mem.used)} ({mem.percent}%)")

    print("\n--- Disk (root) ---")
    disk = psutil.disk_usage("/")
    print(f"Total: {human_readable(disk.total)}")
    print(f"Used:  {human_readable(disk.used)} ({disk.percent}%)")
    print(f"Free:  {human_readable(disk.free)}")

    print("\n--- Battery ---")
    battery = psutil.sensors_battery() if hasattr(psutil, "sensors_battery") else None
    if battery:
        plugged = "Plugged in" if battery.power_plugged else "On battery"
        print(f"Charge: {battery.percent}% ({plugged})")
    else:
        print("No battery detected (or unsupported on this system).")


if __name__ == "__main__":
    main()
