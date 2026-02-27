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
