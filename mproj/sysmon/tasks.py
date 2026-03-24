#!/usr/bin/env python3
import datetime
from celery import shared_task
from diskinfo import FileSystem
from .utils import get_memory_info, get_cpu_info, get_disk_info
from .models import MemoryData, CpuData, CpuUsageData, DiskData, DiskUsageData, PartitionData, FilesystemData, FilesystemUsageData, Settings
from django.utils import timezone

@shared_task
def database_cleanup():
    settings, _ = Settings.objects.get_or_create(pk=1)
    if settings.retention_period is None:
        return
    else:
        limit = timezone.now() - settings.retention_period
        DiskUsageData.objects.filter(timestamp__lte=limit).delete()
        FilesystemUsageData.objects.filter(timestamp__lte=limit).delete()
        CpuUsageData.objects.filter(timestamp__lte=limit).delete()
        MemoryData.objects.filter(timestamp__lte=limit).delete()
        return

@shared_task
def check_memory_and_cpu():
    # Check memory data
    stats: dict[str, str | float | dict[str, str]] = get_memory_info()
    s: MemoryData = MemoryData(timestamp=timezone.now(), free=stats['free_memory'], total=stats["total_memory"])
    s.save()
    # Check CPU data
    statsCpu: dict[str, str | list[float]] = get_cpu_info()
    time = timezone.now()
    sCpu = CpuData(timestamp=time, avg_load=statsCpu["avg_load"])
    sCpu.save()
    s2 = []
    all_zeroes = True
    for i, v in enumerate(statsCpu['cpu_usage']):
        s2.append(CpuUsageData(cpu_data=sCpu, cpu_usage=v, cpu_number=i))
        if v != 0.00:
            all_zeroes = False
    if not all_zeroes:
        CpuUsageData.objects.bulk_create(s2)
    # Check disk data
    dud = []
    fud = []
    disks = []
    partitions = []
    statsDisk = get_disk_info()
    active_hw_ids = []
    active_part_uuids = []
    filesystems = []
    active_fs_uuids = []
    for disk in statsDisk:
        hw_id = disk['wwn'] or disk['serial'] or disk['device']
        active_hw_ids.append(hw_id)
        diskObject = DiskData(
            hw_id=hw_id,
            hw_id_type='wwn' if disk['wwn'] else ('serial' if disk['serial'] else 'device'),
            device=disk['device'],
            active=True,
            type=disk['type'],
        )
        disks.append(diskObject)
    # Check for active disks - we need to deactivate them if they are not attached
    activeDisks = DiskData.objects.filter(active=True)
    for diskOb in activeDisks:
        if diskOb.hw_id not in active_hw_ids:
            diskOb.active = False
            disks.append(diskOb)
    DiskData.objects.bulk_create(
        disks,
        update_conflicts=True,
        unique_fields=['hw_id'],
        update_fields=['device', 'active'],
    )
            
    disksDb = {disk.hw_id: disk for disk in DiskData.objects.all()}
    
    for disk in statsDisk:
        hw_id = disk['wwn'] or disk['serial'] or disk['device']
        dud.append(DiskUsageData(
            device = disksDb[hw_id],
            timestamp = time,
            total = disk['size'],
            read_count = disk['read_count'],
            write_count = disk['write_count'],
            read_bytes = disk['read_bytes'],
            write_bytes = disk['write_bytes'],
        ))
        for partition in disk['partitions']:
            if partition['uuid']:
                partitionObject = PartitionData(
                    device = disksDb[hw_id],
                    uuid = partition['uuid'],
                    active = True,
                    name = partition['name'],
                    total = partition['size'],
                )
                active_part_uuids.append(partition['uuid'])
                partitions.append(partitionObject)
    activePartitions = PartitionData.objects.filter(active=True)
    for partitionOb in activePartitions:
        if partitionOb.uuid not in active_part_uuids:
            partitionOb.active = False
            partitions.append(partitionOb)
    PartitionData.objects.bulk_create(
        partitions,
        update_conflicts=True,
        unique_fields=['uuid'],
        update_fields=['active', 'device', 'name', 'total']
    )
    DiskUsageData.objects.bulk_create(dud)
    partitionDb = {partition.uuid: partition for partition in PartitionData.objects.all()}
    for disk in statsDisk:
        hw_id = disk['wwn'] or disk['serial'] or disk['device']
        if disk['filesystem']:
            fs = FilesystemData(
                disk = disksDb[hw_id],
                label = disk['filesystem']['label'],
                mount_point = disk['filesystem']['mount_point'],
                uuid = disk['filesystem']['uuid'],
                active = True,
                filesystem_type = disk['filesystem']['filesystem_type']
            )
            filesystems.append(fs)
            active_fs_uuids.append(disk['filesystem']['uuid'])
        else:
            for partition in disk['partitions']:
                if partition['filesystem']:
                    fs = FilesystemData(
                        partition = partitionDb[partition['uuid']],
                        label = partition['filesystem']['label'],
                        mount_point = partition['filesystem']['mount_point'],
                        uuid = partition['filesystem']['uuid'],
                        active = True,
                        filesystem_type = partition['filesystem']['filesystem_type']
                    )
                    filesystems.append(fs)
                    active_fs_uuids.append(partition['filesystem']['uuid'])
    activeFilesystems = FilesystemData.objects.filter(active=True)
    for filesystemOb in activeFilesystems:
        if filesystemOb.uuid not in active_fs_uuids:
            filesystemOb.active = False
            filesystems.append(filesystemOb)
    FilesystemData.objects.bulk_create(
        filesystems,
        update_conflicts=True,
        unique_fields=['uuid'],
        update_fields=['active', 'mount_point', 'label']
    )
    filesystemDb = {filesystem.uuid: filesystem for filesystem in FilesystemData.objects.all()}
    for disk in statsDisk:
        hw_id = disk['wwn'] or disk['serial'] or disk['device']
        if disk['filesystem']:
            item = FilesystemUsageData(
                filesystem = filesystemDb[disk['filesystem']['uuid']],
                timestamp = time,
                size = disk['filesystem']['size'],
                free = disk['filesystem']['free_space'],
            )
            fud.append(item)
        else:
            for partition in disk['partitions']:
                if partition['filesystem']:
                    item = FilesystemUsageData(
                        filesystem = filesystemDb[partition['filesystem']['uuid']],
                        timestamp = time,
                        size = partition['filesystem']['size'],
                        free = partition['filesystem']['free_space'],
                    )
                    fud.append(item)

    FilesystemUsageData.objects.bulk_create(fud)
