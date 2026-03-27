#!/usr/bin/env bash
export HOST_NAME=$(hostname)

usage() {
    echo "Usage"
    echo "start.sh [-d|D]"
    echo "Options:"
    echo "-d:  Shut down the app"
    echo "-D:  Manage the development version of the app"
}


if command -v docker >/dev/null 2>&1
then
    COMMAND=docker
elif command -v podman >/dev/null 2>&1
then
    COMMAND=podman
else
    echo "Docker not found. Aborting."
    exit 1
fi

DOCKERFILE=docker-compose.prod.yaml
ARGUMENTS="up --build -d"

while getopts ":dDh" option; do
    case $option in
        D)
            DOCKERFILE=docker-compose.yaml;;
        d)
            ARGUMENTS=down;;
        h)
            usage;
            exit;;
        \?)
            echo "Error: Invalid option.";
            usage
            exit 1;;
    esac
done

$COMMAND compose -f $DOCKERFILE $ARGUMENTS
