#!/bin/bash

set -e

ARGS=$@
scripts/git-hooks.sh
docker compose build
docker compose up $ARGS