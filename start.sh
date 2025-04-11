#!/bin/bash

# Safe production server setup
exec gunicorn main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${PORT:-10000} \
    --timeout 60 \
    --max-requests 100 \
    --log-level info
