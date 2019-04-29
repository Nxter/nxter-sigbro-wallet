#!/bin/bash

NUM_WORKERS=1
TIMEOUT=120
PORT=8020

GUNICORN_CMD_ARGS="--bind=0.0.0.0:$PORT --timeout $TIMEOUT --workers=$NUM_WORKERS --log-level=debug --reload" gunicorn main:routes.app 

