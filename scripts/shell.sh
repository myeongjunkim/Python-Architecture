#!/bin/bash

scripts/git-hooks.sh
docker compose build
docker compose run --rm app /bin/bash