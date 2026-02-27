#!/usr/bin/env python3

from django.urls import path
from rest_framework .urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("uptime", views.uptime, name="uptime"),
    path("memory", views.memory, name="memory"),
    path("cpu/<int:time>", views.cpu, name="cpu"),
    path("time", views.time, name="time"),
    path("memory/<int:pk>", views.memory_detail, name="memorydrf_detail"),
    path("memory_history/<int:time>", views.memory_history, name="memory_history"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
