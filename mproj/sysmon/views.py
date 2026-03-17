from datetime import datetime, timedelta
from types import NoneType
from django.db.models import Prefetch
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from rest_framework.exceptions import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.request import Request

from .models import DiskUsageData, MemoryData, CpuData, DiskData, PartitionData, FilesystemUsageData, FilesystemData
from .utils import get_cpu_info, get_system_time, get_uptime, get_hostname
from .serializer import CpuDataSerializer, MemorySerializer, SystemInfoSerializer, DiskDataSerializer

@api_view(['GET'])
def uptime(request: Request) -> Response:
    return Response({
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

            recent_fud = FilesystemUsageData.objects.filter(timestamp__gt=time_threshold)
            recent_dud = DiskUsageData.objects.filter(timestamp__gt=time_threshold)

            filesystems_with_recent_fud = Prefetch(
                'filesystem_data',
                queryset=FilesystemData.objects.prefetch_related(
                    Prefetch('filesystem_usage',
                             queryset=recent_fud)
                )
            )
            data = DiskData.objects.prefetch_related(
                Prefetch(
                    'disk_usage',
                    queryset=recent_dud,
                ),
                filesystems_with_recent_fud,
                Prefetch(
                    'partition_data',
                    queryset=PartitionData.objects.prefetch_related(
                            filesystems_with_recent_fud,
                    )
                )
            )
            s = DiskDataSerializer(data, many=True)
        else:
            data = DiskData.objects.all()
            s = DiskDataSerializer(data, many=True)
        return Response(s.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def time(request: Request) -> Response:
    system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
    return Response(system_time)

class SystemInfoView(APIView):
    def get(self, request: Request) -> Response:
        system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
        uptime = round(get_uptime(), 2)
        data = {
            "system_time": system_time['date_and_time'],
            "uptime": uptime,
            "system_time_zone": system_time["time_zone_name"],
            "system_time_offset": system_time["time_zone_offset"],
            "cpu_model": get_cpu_info()['cpu_model'],
            "hostname": get_hostname(),
        }
        s = SystemInfoSerializer(data)
        return Response(s.data)

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            response.set_cookie('refresh_token',
                                value=refresh_token,
                                httponly=True,
                                max_age= 24 * 60 * 60 * 7
                                )
            del response.data['refresh']
        return response

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)

@api_view(['GET'])
def logout(request: Request) -> Response:
    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie('refresh_token')
    return response
