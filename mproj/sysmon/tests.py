from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

# Create your tests here.

class SysmonAPITest(TestCase):
   def setUp(self) -> None:
        self.client = Client()

   @patch('sysmon.views.get_uptime')
   def test_uptime_endpoint(self, mock_get_uptime) -> None:
        mock_get_uptime.return_value = 100.0

        response = self.client.get(reverse("uptime"))

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['uptime_minutes'], 100.0)

   @patch('sysmon.views.get_memory_info')
   def test_memory_endpoint(self, mock_get_memory) -> None:
        mock_get_memory.return_value = {
            "free_memory" : "50000",
            "total_memory": "100000",
            "used_percent" : 50.0
        }

        response = self.client.get(reverse("memory"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['free_memory'], "50000")
        self.assertEqual(response.json()['total_memory'], "100000")
        self.assertEqual(response.json()['used_percent'], 50.0)

   @patch('sysmon.views.get_cpu_info')
   def test_cpu_endpoint(self, mock_get_cpu) -> None:
        mock_get_cpu.return_value = {
            "avg_load": "0.06",
            "cpu_model": "Intel FakeCPU"
        }

        response = self.client.get(reverse("cpu"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['avg_load'], "0.06")
        self.assertEqual(response.json()['cpu_model'], "Intel FakeCPU")
