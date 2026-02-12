from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .utils import get_cpu_info, get_memory_info, get_uptime

# Create your views here.

def uptime(request):
    # Get the uptime info
    #r = f"Uptime: {get_uptime():.2f}m"
    return JsonResponse({
        "uptime_minutes": round(get_uptime(), 2),
        "status": "OK"
    }
    )

def memory(request):
    stats = get_memory_info()
    return JsonResponse(stats)

def cpu(request):
    stats = get_cpu_info()
    return JsonResponse(stats)
