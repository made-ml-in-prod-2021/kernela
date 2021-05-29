#!/usr/bin/env sh
set -eu
./wait-it.sh --host="postgres" --port="5432"
exec "$@"