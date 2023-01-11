#!/bin/bash

set -e

poetry install --sync

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000