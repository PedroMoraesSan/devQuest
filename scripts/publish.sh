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

VERSION="$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")"
TARGET="${1:-pypi}"

if [[ "$TARGET" == "test" || "$TARGET" == "testpypi" ]]; then
  INDEX_URL="https://test.pypi.org/pypi/devquest/json"
  UPLOAD_REPO="testpypi"
else
  INDEX_URL="https://pypi.org/pypi/devquest/json"
  UPLOAD_REPO=""
fi

if python - "$INDEX_URL" "$VERSION" <<'PY'
import json
import sys
import urllib.request

url, version = sys.argv[1], sys.argv[2]
try:
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.load(resp)
except Exception:
    sys.exit(0)  # package missing or network issue — let twine decide

if version in data.get("releases", {}):
    print(f"ERROR: version {version} already exists on the index.")
    print("Bump version in pyproject.toml, then run this script again.")
    sys.exit(1)
PY
then
  :
else
  exit 1
fi

echo "Publishing devquest==${VERSION} ..."

python -m pip install -q build twine
rm -rf dist/ build/
python -m build

if [[ -n "$UPLOAD_REPO" ]]; then
  twine upload --repository "$UPLOAD_REPO" dist/*
else
  twine upload dist/*
fi

echo "Done. https://pypi.org/project/devquest/${VERSION}/"
