from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.exceptions import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import MemoryData, CpuData, CpuUsageData
from .utils import get_system_time, get_uptime
from .serializer import CpuDataSerializer, MemorySerializer, CpuUsageDataSerializer
from rest_framework.parsers import JSONParser


def uptime(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "uptime_minutes": round(get_uptime(), 2),
        "status": "OK"
    }
    )

@api_view(['GET'])
def memory(request, format=None):
    if request.method == 'GET':
        mem = MemoryData.objects.all()
        s = MemorySerializer(mem, many=True)
        return Response(s.data)

@api_view(['GET'])
def memory_history(request, time, format=None):
    if request.method == 'GET':
        mem = MemoryData.objects.filter(timestamp__gt=timezone.now()-timedelta(minutes=time)).order_by("timestamp")
        s = MemorySerializer(mem, many=True)
        return Response(s.data)

@api_view(['GET'])
def memory_detail(request, pk, format=None):
    try:
        mem = MemoryData.objects.get(pk=pk)
    except MemoryData.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        s = MemorySerializer(mem)
        return Response(s.data)

@api_view(['GET'])
def cpu(request, time, format=None) -> Response:
    if request.method == 'GET':
        data = CpuData.objects.filter(timestamp__gt=timezone.now()-timedelta(minutes=time)).order_by("timestamp")
        s = CpuDataSerializer(data, many=True)
        return Response(s.data)

def time(request: HttpRequest) -> JsonResponse:
    system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
    return JsonResponse(system_time)
