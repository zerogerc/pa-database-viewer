#!/usr/bin/env bash

PYTHONPATH=. python3 server/main.py \
    --pa-db-path="data/pa-covid.db" \
    --debug
