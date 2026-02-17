from datetime import date, datetime, timedelta
from django.http import HttpRequest, JsonResponse

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
    stats: dict[str, str | float] = get_memory_info()
    s = MemoryData(timestamp=datetime.now(), free=stats['free_memory'], total=stats["total_memory"])
    s.save()
    return JsonResponse(stats)

def cpu(request: HttpRequest) -> JsonResponse:
    stats: dict[str, str] = get_cpu_info()
    s = CpuData(timestamp=datetime.now(), avg_load=stats["avg_load"])
    s.save()
    return JsonResponse(stats)

def time(request: HttpRequest) -> JsonResponse:
    system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
    return JsonResponse(system_time)
