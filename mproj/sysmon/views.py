from datetime import datetime, timedelta
from types import NoneType
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.exceptions import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import DiskUsageData, MemoryData, CpuData, DiskData, PartitionUsageData, PartitionData
from .utils import get_cpu_info, get_system_time, get_uptime
from .serializer import CpuDataSerializer, MemorySerializer, SystemInfoSerializer, DiskDataSerializer
from rest_framework.parsers import JSONParser


def uptime(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "uptime_minutes": round(get_uptime(), 2),
        "status": "OK"
    }
    )

@api_view(['GET'])
def memory(request, time: int | NoneType = None, format=None):
    if request.method == 'GET':
        if time is not None:
            data = MemoryData.objects.filter(timestamp__gt=timezone.now()-timedelta(minutes=time)).order_by("timestamp")
            s = MemorySerializer(data, many=True)
        else:
            data = MemoryData.objects.all()
            s = MemorySerializer(data, many=True)
        return Response(s.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def memory_detail(request, pk, format=None):
    try:
        mem = MemoryData.objects.get(pk=pk)
    except MemoryData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        s = MemorySerializer(mem)
        return Response(s.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cpu(request, time: int | NoneType = None, format=None) -> Response:
    if request.method == 'GET':
        if time is not None:
            data = CpuData.objects.filter(timestamp__gt=timezone.now()-timedelta(minutes=time)).order_by("timestamp")
            s = CpuDataSerializer(data, many=True)
        else:
            data = CpuData.objects.all()
            s = CpuDataSerializer(data, many=True)
        return Response(s.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def disk(request, time: int | NoneType = None, format=None) -> Response:
    if request.method == 'GET':
        if time is not None:
            time_threshold = timezone.now() - timedelta(minutes=time)
            recent_pud = PartitionUsageData.objects.filter(timestamp__gt=time_threshold)
            recent_dud = DiskUsageData.objects.filter(timestamp__gt=time_threshold)
            partitions_with_recent_pud = Prefetch(
                'partition_data',
                queryset=PartitionData.objects.prefetch_related(
                    Prefetch('partition_usage',
                             queryset=recent_pud)
                )
            )
            data = DiskData.objects.prefetch_related(
                Prefetch(
                    'disk_usage',
                    queryset=recent_dud,
                ),
                partitions_with_recent_pud
            )
            s = DiskDataSerializer(data, many=True)
        else:
            data = DiskData.objects.all()
            s = DiskDataSerializer(data, many=True)
        return Response(s.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

def time(request: HttpRequest) -> JsonResponse:
    system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
    return JsonResponse(system_time)

class SystemInfoView(APIView):
    def get(self, request):
        system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
        uptime = round(get_uptime(), 2)
        data = {
            "system_time": system_time['date_and_time'],
            "uptime": uptime,
            "system_time_zone": system_time["time_zone_name"],
            "system_time_offset": system_time["time_zone_offset"],
            "cpu_model": get_cpu_info()['cpu_model'],
        }
        s = SystemInfoSerializer(data)
        return Response(s.data)
