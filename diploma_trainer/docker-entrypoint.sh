#!/bin/sh
set -e

# Проверяем, запущен ли Docker демон
if !docker info >/dev/null 2>&1; then
    # Если не запущен, запускаем Docker демон
    dockerd --host=unix:///var/run/docker.sock &
    # Ожидаем, пока Docker демон будет доступен
    until docker info >/dev/null 2>&1; do
        sleep 1
    done
fi

exec "$@"
