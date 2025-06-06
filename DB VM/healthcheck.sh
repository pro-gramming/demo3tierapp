#!/bin/bash
set -e

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is not running"
    exit 1
fi

# Check if nginx is running
if ! pgrep -x "nginx" > /dev/null; then
    echo "Nginx is not running"
    exit 1
fi

# Check if supervisor is running
if ! pgrep -x "supervisord" > /dev/null; then
    echo "Supervisord is not running"
    exit 1
fi

# All checks passed
exit 0 