#!/bin/sh
set -e

# Start Nginx
nginx -g "daemon off;" &

# Start Gunicorn
/app/gunicorn.start 