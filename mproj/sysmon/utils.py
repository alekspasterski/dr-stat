#!/usr/bin/env python3


def get_uptime():
    try:
        with open("/proc/uptime", "r") as uptime_file:
            uptime = uptime_file.read()
        uptime = uptime.split(" ")
    except FileNotFoundError:
        return -1
    return float(uptime[0]) / 60.0

# Returns various information about memory as a dictionary
def get_memory_info():
    # Set defaults
    free_memory = -1
    total_memory = -1
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

def get_cpu_info():
    avg_load = -1
    cpu_model = "Unknown CPU"
    try:
        with open("/proc/loadavg", "r") as cpu_file:
            for line in cpu_file:
                avg_load = line.split()[0]
    except FileNotFoundError:
        avg_load = -1
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
