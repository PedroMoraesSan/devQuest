# Publishing DevQuest to PyPI

## Security rules

- Never commit the PyPI API token.
- Never put the token in `pyproject.toml`, scripts, or chat logs.
- Prefer a **project-scoped** token on PyPI (not a full-account token).
- Use an environment variable for upload only.

If you already used a full-account token, rotate it after publishing and create a project-scoped one.

## One-time setup

```bash
pip install build twine
```

## Build

```bash
rm -rf dist/ build/
python -m build
```

## Upload (safe)

Put the token in `.env` at the repo root (gitignored — see `.env.example`):

```bash
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-...
```

Then:

```bash
./scripts/publish.sh          # real PyPI
./scripts/publish.sh test     # TestPyPI
```

Or export in the shell for a one-off upload (do not commit):

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD='pypi-...'
twine upload dist/*
```

## Verify

```bash
pip install devquest
hero --help
```

## Next release

1. Bump `version` in `pyproject.toml`
2. Rebuild: `python -m build`
3. Upload: `twine upload dist/*`
4. Tag: `git tag vX.Y.Z && git push --tags`
