#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$DIR"

# Repassa todos os argumentos para o Python
python3 src/main.py "$@"
