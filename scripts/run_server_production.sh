#!/usr/bin/env bash

cd client && yarn build && cd ..

PYTHONPATH=. python3 server/main.py \
    --pa-db-path="data/pa-covid.db" \
    --index-path="/Users/Uladzislau.Sazanovich/dev/pa-database-viewer/client/build/index.html" \
    --static-dir="/Users/Uladzislau.Sazanovich/dev/pa-database-viewer/client/build/static" \
