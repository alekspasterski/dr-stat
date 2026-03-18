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

def clean_mount_point(mount_point: str) -> str:
    if not mount_point:
        return ''
    else:
        mount_point = mount_point.removeprefix('/host')
        return mount_point if mount_point != '' else '/'

def get_disk_info():
    disks = DiskInfo().get_disk_list()
    disks_return = []
    io_counters = psutil.disk_io_counters(perdisk=True)
    ps_partitions = psutil.disk_partitions(all=True)
    for disk in disks:
        d = {
            "wwn": disk.get_wwn(),
            "device": disk.get_name(),
            "serial": disk.get_serial_number(),
            "size": disk.get_size() * 512,
            "read_count": io_counters[disk.get_name()].read_count,
            "write_count": io_counters[disk.get_name()].write_count,
            "read_bytes": io_counters[disk.get_name()].read_bytes,
            "write_bytes": io_counters[disk.get_name()].write_bytes,
            "filesystem": {
            },
            "partitions": [{
                "name": partition.get_name(),
                "uuid": partition.get_part_uuid(),
                #"mount_point": (mp := next((p.mountpoint for p in ps_partitions if p.device == partition.get_path() and p.mountpoint.startswith('/host')), "")) and (mp.removeprefix('/host') or '/'),
                "filesystem": {
                    "uuid": partition.get_filesystem().get_fs_uuid(),
                    "free_space": partition.get_filesystem().get_fs_free_size() * 512,
                    "filesystem_type": partition.get_filesystem().get_fs_type(),
                    "label": partition.get_filesystem().get_fs_label(),
                    "mount_point": clean_mount_point(partition.get_filesystem().get_fs_mounting_point()),
                    "size": partition.get_filesystem().get_fs_size() * 512,
                },
                "size": partition.get_part_size() * 512,
            } for partition in disk.get_partition_list()]
        }
        if disk.get_filesystem():
            disk_filesystem = disk.get_filesystem()
            d_fs = {
                "uuid": disk_filesystem.get_fs_uuid(),
                "free_space": disk_filesystem.get_fs_free_size() * 512,
                "filesystem_type": disk_filesystem.get_fs_type(),
                "label": disk_filesystem.get_fs_label(),
                "mount_point": clean_mount_point(disk_filesystem.get_fs_mounting_point()),
                "size": disk_filesystem.get_fs_size() * 512,
                }
            d.update({'filesystem': d_fs})
        disks_return.append(d)
    return disks_return

def get_hostname() -> str:
    hostname = ""
    try:
        with open("/etc/hostname", "r") as hostname_file:
            hostname = hostname_file.readline().strip()
    except FileNotFoundError:
        hostname = ""
    return hostname
