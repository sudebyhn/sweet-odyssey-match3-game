#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
    exec python3 app.py "$@"
elif command -v python >/dev/null 2>&1; then
    exec python app.py "$@"
else
    printf '%s\n' 'Python 3.11 veya üzeri gerekiyor: https://www.python.org/downloads/'
    exit 1
fi
