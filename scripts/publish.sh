#!/usr/bin/env bash
# Build and upload DevQuest to PyPI.
# Requires TWINE_PASSWORD in the environment. Never hardcode tokens here.

set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -z "${TWINE_PASSWORD:-}" ]]; then
  echo "Missing TWINE_PASSWORD."
  echo "Export your PyPI token first:"
  echo "  export TWINE_USERNAME=__token__"
  echo "  export TWINE_PASSWORD='pypi-...'"
  exit 1
fi

export TWINE_USERNAME="${TWINE_USERNAME:-__token__}"

python -m pip install -q build twine
rm -rf dist/ build/
python -m build

TARGET="${1:-pypi}"

if [[ "$TARGET" == "test" || "$TARGET" == "testpypi" ]]; then
  twine upload --repository testpypi dist/*
else
  twine upload dist/*
fi

echo "Done. Unset the token: unset TWINE_PASSWORD"
