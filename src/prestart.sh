#! /usr/bin/env bash

# Let the DB start
python3 /zkit/backend_pre_start.py

# Run migrations
alembic upgrade head

exec "$@"
