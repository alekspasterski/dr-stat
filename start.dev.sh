#!/usr/bin/env bash
export HOST_NAME=$(hostname)

podman compose -f docker-compose.yaml up --build -d
