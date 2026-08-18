#!/bin/bash

set -e
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="$SCRIPT_DIR/profile"
WORK="/archiso-work"
OUTPUT="$SCRIPT_DIR/out"

mkarchiso \
    -v \
    -r \
    -A "Dashed" \
    -L "DASHED" \
    -w "$WORK" \
    -o "$OUTPUT" \
    "$PROFILE"

echo "Output:"
ls -lh "$OUTPUT"