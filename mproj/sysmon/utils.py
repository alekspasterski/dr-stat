#!/usr/bin/env python3
from datetime import datetime, tzinfo, timezone, timedelta


def get_uptime() -> float:
    try:
        with open("/proc/uptime", "r") as uptime_file:
            uptime: str = uptime_file.read()
        uptime_lines: list[str] = uptime.split()
    except FileNotFoundError:
        return -1.0
    return float(uptime_lines[0]) / 60.0

# Returns various information about memory as a dictionary
def get_memory_info() -> dict[str, int | float]:
    # Set defaults
    free_memory: int = -1
    total_memory: int = -1
    # Get the info from meminfo
    try:
        with open("/proc/meminfo", "r") as mem_file:
            for line in mem_file:
                if "MemAvailable:" in line:
                    free_memory = int(line.split()[1])
                elif "MemTotal:" in line:
                    total_memory = int(line.split()[1])
        if total_memory > 0:
            used_percent = (1 - (free_memory / total_memory)) * 100
        else:
            used_percent = 0.0
        return {
            "free_memory" : free_memory,
            "total_memory" : total_memory,
            "used_percent": used_percent
        }
    except (FileNotFoundError, ValueError, ZeroDivisionError, IndexError):
        return {
            "free_memory" : -1,
            "total_memory" : -1,
            "used_percent": -1.0
        }

def get_cpu_info() -> dict[str, str]:
    avg_load = "Error"
    cpu_model = "Unknown CPU"
    try:
        with open("/proc/loadavg", "r") as cpu_file:
            for line in cpu_file:
                avg_load = line.split()[0]
    except FileNotFoundError:
        avg_load = "Error"
    try:
        with open("/proc/cpuinfo", "r") as cpu_file:
            for line in cpu_file:
                if "model name" in line:
                    cpu_model = " ".join(line.split()[3:])
                    break
    except FileNotFoundError:
        cpu_model = "Unknown CPU"
    return({
        "avg_load" : avg_load,
        "cpu_model" : cpu_model,
    })

def get_system_time() -> dict[str, datetime | str | timedelta | None]:
    current_system_time: datetime = datetime.now().astimezone()
    return({
        "date_and_time": current_system_time,
        "time_zone_name": current_system_time.tzname(),
        "time_zone_offset": current_system_time.utcoffset(),
    })
