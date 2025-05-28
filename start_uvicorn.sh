#!/bin/bash
source digitalizador-venv/bin/activate
PYTHONPATH=. uvicorn main:create_app --host 0.0.0.0 --port 8086 --factory
