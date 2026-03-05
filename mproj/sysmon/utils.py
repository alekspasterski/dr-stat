#!/usr/bin/env python3
from datetime import datetime, timedelta
import psutil
from platform import system
from diskinfo import DiskInfo, disksmart


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

def get_cpu_info() -> dict[str, str | list[float]]:
    avg_load : str = "Error"
    cpu_model : str = "Unknown CPU"
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

    cpu_usage : list[float] = psutil.cpu_percent(percpu=True)
    
    return({
        "avg_load" : avg_load,
        "cpu_model" : cpu_model,
        "cpu_usage" : cpu_usage,
    })

def get_system_time() -> dict[str, datetime | str | timedelta | None]:
    current_system_time: datetime = datetime.now().astimezone()
    return({
        "date_and_time": current_system_time,
        "time_zone_name": current_system_time.tzname(),
        "time_zone_offset": current_system_time.utcoffset(),
    })

def get_disk_info():
    disks = DiskInfo().get_disk_list()
    disks_return = []
    io_counters = psutil.disk_io_counters(perdisk=True)
    ps_partitions = psutil.disk_partitions(all=True)
    for item in disks:
        d = {
            "wwn": item.get_wwn(),
            "device": item.get_name(),
            "serial": item.get_serial_number(),
            "size": item.get_size() * 512,
            "read_count": io_counters[item.get_name()].read_count,
            "write_count": io_counters[item.get_name()].write_count,
            "read_bytes": io_counters[item.get_name()].read_bytes,
            "write_bytes": io_counters[item.get_name()].write_bytes,
            "partitions": [{
                "mount_point": (mp := next((p.mountpoint for p in ps_partitions if p.device == partition.get_path() and p.mountpoint.startswith('/host')), "")) and (mp.removeprefix('/host') or '/'),
                "filesystem": partition.get_fs_type(),
                "uuid": partition.get_fs_uuid(),
                "size": partition.get_part_size() * 512,
                "free_space": partition.get_fs_free_size() * 512,
            } for partition in item.get_partition_list()]
        }
        disks_return.append(d)
    return disks_return
