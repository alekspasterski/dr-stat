#!/usr/bin/env python3
from celery import shared_task
from .utils import get_memory_info, get_cpu_info, get_disk_info
from .models import MemoryData, CpuData, CpuUsageData, DiskData, DiskUsageData, PartitionData, PartitionUsageData
from django.utils import timezone


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
    pud = []
    disks = []
    partitions = []
    statsDisk = get_disk_info()
    active_hw_ids = []
    active_part_uuids = []
    for disk in statsDisk:
        hw_id = disk['wwn'] or disk['serial'] or disk['device']
        active_hw_ids.append(hw_id)
        diskObject = DiskData(
            hw_id=hw_id,
            hw_id_type='wwn' if disk['wwn'] else ('serial' if disk['serial'] else 'device'),
            device=disk['device'],
            active=True
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
#        hw_id = disk['wwn'] if disk['wwn'] != '' else disk['serial']
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
                    mount_point = partition['mount_point'],
                    filesystem = partition['filesystem'],
                    uuid = partition['uuid'],
                    active = True,
                    name = partition['name'],
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
        update_fields=['mount_point', 'filesystem', 'active', 'device', 'name']
    )
    DiskUsageData.objects.bulk_create(dud)
    partitionsDb = {partition.uuid: partition for partition in PartitionData.objects.all()}
    for disk in statsDisk:
        for partition in disk['partitions']:
            if partition['uuid']:
                partitionObject = partitionsDb[partition['uuid']]
                partitionUsageObject = PartitionUsageData(
                    partition = partitionObject,
                    timestamp = time,
                    total = partition['size'],
                    free = partition['free_space'],
                )
                pud.append(partitionUsageObject)
    PartitionUsageData.objects.bulk_create(pud)
