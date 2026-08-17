#!/bin/bash

set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ISO="$(find "$SCRIPT_DIR/out" -maxdepth 1 -name '*.iso' -print -quit)"

if [[ -z "$ISO" ]]; then
    echo "No ISO found."
    echo "Run ./build.sh first."
    exit 1
fi

run_archiso -i "$ISO"