#!/bin/bash

if [ "${DEBUG}" == "1" ]; then
        echo "Starting in Debug mode"
        uvicorn app.main:app --host 0.0.0.0 --port 2090 --reload
else
        echo "Starting in Production mode"
        uvicorn app.main:app --host 0.0.0.0 --port 2090
fi
