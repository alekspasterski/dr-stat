from django.db import models

class MemoryData(models.Model):
    timestamp = models.DateTimeField()
    free = models.DecimalField(decimal_places=0, max_digits=100)
    total = models.DecimalField(decimal_places=0, max_digits=100)

    def __str__(self):
        return self.timestamp.isoformat()

class CpuData(models.Model):
    timestamp = models.DateTimeField()
    avg_load = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return self.timestamp.isoformat()

class CpuUsageData(models.Model):
    cpu_data = models.ForeignKey(CpuData, related_name='cpu_usage', on_delete=models.CASCADE)
    cpu_number = models.IntegerField()
    cpu_usage = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return f"CPU: {self.cpu_number}, Usage: {self.cpu_usage}"

class DiskData(models.Model):
    hw_id = models.CharField(unique=True)
    hw_id_type = models.CharField()
    device = models.CharField()
    active = models.BooleanField()
    type = models.CharField()
    def __str__(self):
        return self.device

class PartitionData(models.Model):
    device = models.ForeignKey(DiskData, related_name="partition_data", on_delete=models.CASCADE)
    name = models.CharField(null=True)
    uuid = models.CharField(unique=True)
    active = models.BooleanField()
    total = models.PositiveBigIntegerField()
    def __str__(self):
        return self.name
    
class FilesystemData(models.Model):
    disk = models.OneToOneField(DiskData, related_name="filesystem_data", on_delete=models.CASCADE, null=True, blank=True)
    partition = models.OneToOneField(PartitionData, related_name="filesystem_data", on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(null=True)
    mount_point = models.CharField()
    uuid = models.CharField(unique=True)
    active = models.BooleanField()
    filesystem_type = models.CharField()

class FilesystemUsageData(models.Model):
    filesystem = models.ForeignKey(FilesystemData, related_name="filesystem_usage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    size = models.BigIntegerField()
    free = models.PositiveBigIntegerField()
    
class DiskUsageData(models.Model):
    device = models.ForeignKey(DiskData, related_name="disk_usage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    total = models.PositiveBigIntegerField()
    read_count = models.PositiveBigIntegerField()
    write_count = models.PositiveBigIntegerField()
    read_bytes = models.PositiveBigIntegerField()
    write_bytes = models.PositiveBigIntegerField()

class Settings(models.Model):
    retention_period = models.DurationField(null=True)
