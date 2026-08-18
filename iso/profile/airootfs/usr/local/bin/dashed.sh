#!/bin/bash

set -e

echo "I WORK"

INSTALLER="/opt/dashed/installer"
REQUIREMENTS="$INSTALLER/backend/requirements.txt"

python -m pip install uvicorn fastapi --break-system-packages

cd "$INSTALLER"

exec python installer.py
