#!/usr/bin/env bash

PYTHONPATH=. python3 server/main.py \
    --pa-db-path="data/pa-covid.db" \
    --index-path="client/build/index.html" \
    --static-dir="client/build/static" \
