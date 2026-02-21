from django.db import models

# Create your models here.
class MemoryData(models.Model):
    timestamp = models.DateTimeField()
    free = models.DecimalField(decimal_places=0, max_digits=100)
    total = models.DecimalField(decimal_places=0, max_digits=100)

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

class CpuData(models.Model):
    timestamp = models.DateTimeField()
    avg_load = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

class CpuUsageData(models.Model):
    timestamp = models.DateTimeField()
    cpu_usage = models.DecimalField(decimal_places=2, max_digits=5)
    cpu_number = models.IntegerField()
    def __str__(self):
        return self.timestamp.isoformat()
