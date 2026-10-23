#!/usr/bin/env bash
# Corre el pipeline completo: xls -> csv -> contratos -> plantillas + reportes
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/ingest.py
python3 scripts/contratos.py
python3 scripts/ventas.py
python3 scripts/plantillas.py "$@"
