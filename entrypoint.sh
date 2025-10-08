#!/bin/sh

# Fail on any error
set -e

echo "Starting entrypoint..."

# Basic checks for required env vars (fail early if missing)
: "${DEV_DB_HOST:?DEV_DB_HOST is not set}"
: "${DEV_DB_USER:?DEV_DB_USER is not set}"
# DEV_DB_PASSWORD may be empty for some setups; don't force it here

echo "Waiting for database at ${DEV_DB_HOST}..."

# If mysqladmin is available prefer it (clean ping). Otherwise fall back
# to a small Python TCP connect loop which doesn't require extra packages.
if command -v mysqladmin >/dev/null 2>&1; then
    echo "Using mysqladmin to wait for DB..."
    while ! mysqladmin ping -h"$DEV_DB_HOST" -u"$DEV_DB_USER" -p"$DEV_DB_PASSWORD" --silent; do
        sleep 1
    done
else
    echo "mysqladmin not found, falling back to Python TCP check"
    # Try to connect to host:3306 until successful (5s interval)
    while true; do
        python - <<'PY'
import socket, os, time
host = os.environ.get('DEV_DB_HOST', 'db')
port = int(os.environ.get('DEV_DB_PORT', '3306'))
try:
        s = socket.create_connection((host, port), timeout=3)
        s.close()
        print('TCP connection to %s:%s succeeded' % (host, port))
        raise SystemExit(0)
except Exception as e:
        print('Waiting for TCP %s:%s — %s' % (host, port, e))
        time.sleep(1)
PY
    if [ $? -ne 0 ]; then
        # python returned non-zero; loop will continue
        sleep 1
    else
        break
    fi
    done
fi

echo "Database is up - continuing..."

# Small extra safety delay
sleep 2

echo "Running database migrations..."
python manage.py migrate --noinput

# Kumpulkan file statis untuk produksi
# Cek jika DJANGO_SETTINGS_MODULE mengandung 'production'
if echo "$DJANGO_SETTINGS_MODULE" | grep -q "production"; then
    echo "Collecting static files for production..."
    python manage.py collectstatic --noinput
fi

# Execute the main command (passed from docker-compose or Dockerfile)
exec "$@"