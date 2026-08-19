#!/bin/bash

set -e

echo "I WORK"

INSTALLER="/opt/dashed/installer"
REQUIREMENTS="$INSTALLER/backend/requirements.txt"

python -m pip install \
    --break-system-packages \
    --no-cache-dir \
    -r "$REQUIREMENTS"

cd "$INSTALLER"

exec python installer.py
