#!/bin/bash
set -e

if [ -f /app/data/db.sqlite3 ]; then
    chown wagtail:wagtail /app/data/db.sqlite3
fi

exec gosu wagtail "$@"
