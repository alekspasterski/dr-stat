from datetime import date, datetime, timedelta
from django.http import HttpRequest, JsonResponse
from django.utils import timezone

from .models import MemoryData, CpuData
from .utils import get_cpu_info, get_memory_info, get_system_time, get_uptime

# Create your views here.

def uptime(request: HttpRequest) -> JsonResponse:
    # Get the uptime info
    return JsonResponse({
        "uptime_minutes": round(get_uptime(), 2),
        "status": "OK"
    }
    )

def memory(request: HttpRequest) -> JsonResponse:
    stats: dict[str, str | float | dict[datetime, str]] = get_memory_info()
    historical_data = MemoryData.objects.filter(timestamp__gt=timezone.now()-timedelta(minutes=1)).order_by("timestamp")
    historical_data_list = {}
    for item in historical_data:
        historical_data_list[item.timestamp.isoformat()] = item.free

    s: MemoryData = MemoryData(timestamp=timezone.now(), free=stats['free_memory'], total=stats["total_memory"])
    s.save()
    stats['history'] = historical_data_list
    return JsonResponse(stats)

def cpu(request: HttpRequest) -> JsonResponse:
    stats: dict[str, str] = get_cpu_info()
    s = CpuData(timestamp=timezone.now(), avg_load=stats["avg_load"])
    s.save()
    return JsonResponse(stats)

def time(request: HttpRequest) -> JsonResponse:
    system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
    return JsonResponse(system_time)
