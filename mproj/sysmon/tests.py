from decimal import Decimal
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from .tasks import check_memory_and_cpu
from .models import DiskData, DiskUsageData, FilesystemData, MemoryData, CpuData, CpuUsageData, PartitionData, Settings, FilesystemUsageData
from datetime import timedelta

class SysmonAPITest(TestCase):
   def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.now = timezone.now()
        # Insert test memory data
        MemoryData.objects.create(
           timestamp=self.now,
           total=1000000,
           free=500000,
        )
        # Insert test CPU data
        CpuData.objects.create(
           timestamp=self.now,
           avg_load=10.3,
        )
        CpuUsageData.objects.create(
           cpu_data=CpuData.objects.first(),
           cpu_number=1,
           cpu_usage=29.6,
        )
        # Insert test Settings
        Settings.objects.create(
           retention_period = timedelta(days=4)
        )
        # Insert test disk data
        self.disk = DiskData.objects.create(
           hw_id = "TestDiskHWID",
           hw_id_type = "wwn",
           device = "/dev/sdb",
           active = True,
           type = "SSD",
        )
        self.partition = PartitionData.objects.create(
           device = self.disk,
           name = "TestPart",
           uuid = "123123-1231-1231",
           active = True,
           total = 1000000,
        )
        self.filesystem = FilesystemData.objects.create(
           partition = self.partition,
           label = "Test Partition",
           mount_point = "/mnt/test/",
           uuid = "12312-12366-4232",
           active = True,
           filesystem_type = "ext4",
        )
        FilesystemUsageData.objects.create(
           filesystem = self.filesystem,
           timestamp = self.now,
           size = 1000000,
           free = 100000,
        )
        DiskUsageData.objects.create(
           device = self.disk,
           timestamp = self.now,
           total = 2000000,
           read_count = 500,
           write_count = 600,
           read_bytes = 2000,
           write_bytes = 4000,
        )
      
   @patch('sysmon.views.get_uptime')
   def test_uptime_endpoint(self, mock_get_uptime) -> None:
        mock_get_uptime.return_value = 100.0

        response = self.client.get(reverse("uptime"))

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['uptime_minutes'], 100.0)

   def test_memory_endpoint(self) -> None:
        response = self.client.get(reverse("memory_all"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['timestamp'], self.now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(response.json()[0]['free'], "500000")
        self.assertEqual(response.json()[0]['total'], "1000000")

   def test_cpu_endpoint(self) -> None:
        response = self.client.get(reverse("cpu_all"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['avg_load'], "10.30")
        self.assertEqual(response.json()[0]['timestamp'], self.now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(response.json()[0]['cpu_usage'][0]['cpu_number'], 1)
        self.assertEqual(response.json()[0]['cpu_usage'][0]['cpu_usage'], "29.60")

   def test_disk_endpoint(self) -> None:
      resp = self.client.get(reverse("disk_history", args=[1])).json()[0]
      self.assertEqual(resp['hw_id'], "TestDiskHWID")
      self.assertEqual(resp['hw_id_type'], "wwn")
      self.assertEqual(resp['partition_data'][0]['active'], True)
      self.assertEqual(resp['partition_data'][0]['total'], 1000000)
      self.assertEqual(resp['partition_data'][0]['filesystem_data'][0]['label'], 'Test Partition')
      self.assertEqual(resp['partition_data'][0]['filesystem_data'][0]['filesystem_usage'][0]['size'], 1000000)
      self.assertEqual(resp['disk_usage'][0]['total'], 2000000)

   def test_settings_endpoint(self) -> None:
      response = self.client.get(reverse("settings"))

      self.assertEqual(response.json()['retention_period'], 24 * 60 * 60 * 4)

class SysmonWorkerTest(TestCase):
   def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

   @patch('sysmon.tasks.get_cpu_info')
   def test_worker_cpu(self, mock_get_cpu) -> None:
      mock_get_cpu.return_value = {
         "avg_load": "2.32",
         "cpu_model": "Fake TestCPU",
         "cpu_usage": [
            10.3,
            22.1,
         ],
         "avg_usage": 34.32,
      }
      check_memory_and_cpu()
      cpu_db_data = CpuData.objects.first()
      self.assertAlmostEqual(cpu_db_data.avg_load, Decimal(2.32))
      self.assertEqual(cpu_db_data.cpu_usage.first().cpu_number, 0)
      self.assertAlmostEqual(cpu_db_data.cpu_usage.first().cpu_usage, Decimal(10.3))

   @patch('sysmon.tasks.get_disk_info')
   def test_worker_disk(self, mock_get_disks) -> None:
      mock_get_disks.return_value = [{
         "wwn": "TestWWN",
         "device": "/dev/sda",
         "serial": "1234535123",
         "size": 1000000,
         "read_count": 2000,
         "write_count": 5000,
         "read_bytes": 12000,
         "write_bytes": 22000,
         "type": "SSD",
         "filesystem": {},
         "partitions": [
            {
               "name": "part1",
               "uuid": "32432-23424-23422",
               "filesystem": {
                  "uuid": "220340-230303",
                  "free_space": 4000,
                  "filesystem_type": "ext4",
                  "label": "TestLabel",
                  "mount_point": "/mnt/test",
                  "size": 10000,
               },
               "size": 10000,
            }
         ]
      }]
      check_memory_and_cpu()
      disks_db_data = DiskData.objects.first()
      self.assertEqual(disks_db_data.hw_id, "TestWWN")
      self.assertEqual(disks_db_data.hw_id_type, "wwn")
      self.assertEqual(disks_db_data.partition_data.first().name, "part1")
      self.assertEqual(disks_db_data.partition_data.first().uuid, "32432-23424-23422")
      self.assertEqual(disks_db_data.partition_data.first().filesystem_data.first().label, "TestLabel")
      self.assertEqual(disks_db_data.partition_data.first().filesystem_data.first().filesystem_usage.first().free, 4000)
      self.assertEqual(disks_db_data.disk_usage.first().total, 1000000)

