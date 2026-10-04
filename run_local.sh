#!/usr/bin/env bash
set -euo pipefail
python -m uvicorn api.index:app --reload --host 127.0.0.1 --port 8000
