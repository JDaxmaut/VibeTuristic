#!/bin/bash
set -e

if [ -f /app/data/db.sqlite3 ]; then
    chown wagtail:wagtail /app/data/db.sqlite3
fi

if [ -d /app/data/media ]; then
    chown -R wagtail:wagtail /app/data/media
fi

exec gosu wagtail "$@"
