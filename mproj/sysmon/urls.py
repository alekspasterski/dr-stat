#!/usr/bin/env python3

from django.urls import path
from rest_framework .urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("uptime", views.uptime, name="uptime"),
    path("cpu/<int:time>", views.cpu, name="cpu_history"),
    path("cpu", views.cpu, name="cpu_all"),
    path("time", views.time, name="time"),
    path("memory/<int:time>", views.memory, name="memory_history"),
    path("memory", views.memory, name="memory_all"),
    path("system_info", views.SystemInfoView.as_view(), name="system_info"),
    path("disk/<int:time>", views.disk, name="disk_history"),
    path("token/", views.CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", views.CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.logout, name="logout"),
    path("update_data_polling/", views.update_data_polling, name="update_data_polling"),
    path("settings/", views.settings, name="settings"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
