#!/usr/bin/env bash
export HOST_NAME=$(hostname)

podman compose -f docker-compose.prod.yaml up --build -d
