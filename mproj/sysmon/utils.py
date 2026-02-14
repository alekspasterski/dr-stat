#!/usr/bin/env python3


def get_uptime() -> float:
    try:
        with open("/proc/uptime", "r") as uptime_file:
            uptime: str = uptime_file.read()
        uptime_lines: list[str] = uptime.split(" ")
    except FileNotFoundError:
        return -1.0
    return float(uptime_lines[0]) / 60.0

# Returns various information about memory as a dictionary
def get_memory_info() -> dict[str, str | float]:
    # Set defaults
    free_memory: str = "Unknown"
    total_memory: str = "Unknown"
    # Get the info from meminfo
    try:
        with open("/proc/meminfo", "r") as mem_file:
            for line in mem_file:
                if "MemAvailable:" in line:
                    free_memory = line.split()[1]
                elif "MemTotal:" in line:
                    total_memory = line.split()[1]
        used_percent = (1 - (int(free_memory) / int(total_memory))) * 100
        return {
            "free_memory" : free_memory,
            "total_memory" : total_memory,
            "used_percent": used_percent}
    except FileNotFoundError:
        return {}

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
    except FileNotFoundError:
        cpu_model = "Unknown CPU"
    return({
        "avg_load" : avg_load,
        "cpu_model" : cpu_model,
    })
