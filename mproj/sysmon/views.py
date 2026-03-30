from datetime import datetime, timedelta
from http.client import responses
from io import RawIOBase
from types import NoneType
from django.conf import Settings
from django.db.models import Prefetch
from django.utils import timezone
from rest_framework.exceptions import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from django.utils.encoding import smart_str
from rest_framework import renderers

from .metrics import renderMetric
from .models import DiskUsageData, MemoryData, CpuData, DiskData, PartitionData, FilesystemUsageData, FilesystemData, Settings
from .utils import get_cpu_info, get_disk_usage, get_memory_info, get_system_time, get_uptime, get_hostname
from .serializer import CpuDataSerializer, MemorySerializer, SettingsSerializer, SystemInfoSerializer, DiskDataSerializer

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
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        system_time: dict[str, datetime | str | timedelta | None] = get_system_time()
        uptime = round(get_uptime(), 2)
        interval = 10
        try:
            task = PeriodicTask.objects.get(task="sysmon.tasks.check_memory_and_cpu")
            interval = task.interval.every
        except PeriodicTask.DoesNotExist:
            interval = 10
            
        data = {
            "system_time": system_time['date_and_time'],
            "uptime": uptime,
            "system_time_zone": system_time["time_zone_name"],
            "system_time_offset": system_time["time_zone_offset"],
            "cpu_model": get_cpu_info()['cpu_model'],
            "hostname": get_hostname(),
            "task_interval": interval,
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

@api_view(['POST'])
def update_data_polling(request: Request) -> Response:
    raw_interval = request.data.get('interval')
    try:
        new_interval = int(raw_interval)
    except (TypeError, ValueError):
        return Response(
            {"error" : "Interval must be a valid number"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=new_interval,
        period=IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.update_or_create(
        name='System polling',
        defaults={
            'task':'sysmon.tasks.check_memory_and_cpu',
            "interval":schedule,
        }
    )
    return Response(status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def settings(request: Request) -> Response:
    settings, _ = Settings.objects.get_or_create(pk=1)

    if request.method == 'GET':
        return Response(SettingsSerializer(settings).data)
    
    elif request.method == 'POST':
        for key, value in request.data.items():
            if hasattr(settings, key) and key not in ['id', '_state']:
                if key == 'retention_period':
                    if value in [None, 0, '0', '']:
                        value = None
                    else:
                        try:
                            value = timedelta(seconds=int(value))
                        except (TypeError, ValueError):
                            continue
                setattr(settings, key, value)

        settings.save()
        return Response(
            status=status.HTTP_200_OK,
        )



class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_str(data, encoding=self.charset)

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([PlainTextRenderer])
def metrics(request: Request) -> Response:
    response_text = ""
    memory = get_memory_info()
    cpu = get_cpu_info()
    disk_usage = get_disk_usage()
    if memory:
        response_text += renderMetric("Memory information",
                                    "bytes",
                                    "gauge",
                                    "sysmon_memory",
                                    {'sysmon_memory{state="free"}': str(memory['free_memory']),
                                    'sysmon_memory{state="total"}': str(memory['total_memory'])})
    if cpu:
        response_text += renderMetric("CPU load",
                                    "",
                                    "gauge",
                                    "sysmon_cpu_load",
                                    {'sysmon_cpu_load{unit="load"}': str(cpu['avg_load']),
                                    'sysmon_cpu_load{unit="percent"}': str(cpu['avg_usage'])})
    if disk_usage:
        response_text += renderMetric("Disk usage",
                                    "percent",
                                    "gauge",
                                    "sysmon_disk_usage",
                                    {'sysmon_disk_usage{device="'+ k +'"}': str(disk_usage[k]) for k in disk_usage})
    return Response(data=response_text)
