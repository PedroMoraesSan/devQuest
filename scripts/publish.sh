#!/usr/bin/env bash
# Build and upload DevQuest to PyPI.
# Loads TWINE_PASSWORD from .env (never commit that file).

set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [[ -z "${TWINE_PASSWORD:-}" ]]; then
  echo "Missing TWINE_PASSWORD."
  echo "Add it to .env (gitignored):"
  echo "  TWINE_USERNAME=__token__"
  echo "  TWINE_PASSWORD=pypi-..."
  echo "Or export it in the shell before running this script."
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

echo "Done."
