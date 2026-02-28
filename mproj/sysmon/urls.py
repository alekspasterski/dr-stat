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
]

urlpatterns = format_suffix_patterns(urlpatterns)
