#!/usr/bin/env python3

from django.urls import path

from . import views

urlpatterns = [
    path("uptime", views.uptime, name="uptime"),
    path("memory", views.memory, name="memory"),
    path("cpu", views.cpu, name="cpu"),
    path("time", views.time, name="time"),
    path("memorydrf", views.memorydrf, name="memorydrf"),
    path("memory/<int:pk>", views.memorydrf_detail, name="memorydrf_detail"),
]
