#!/bin/bash
set -euo pipefail

#uvicorn tg_bot.main:main --host 0.0.0.0 --port 8000 --reload
python -m tg_bot.main