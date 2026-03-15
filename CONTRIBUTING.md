# Contributing

## Setup

```bash
python3 -m pip install -e .[dev]
```

## Test

Run the unit test suite before opening a pull request:

```bash
python3 -m pytest -q
python3 -m build
```

## Live API Checks

Live generation tests are optional and require Higgsfield credentials:

```bash
export HF_API_KEY="your-key"
export HF_API_SECRET="your-secret"
python3 examples/simple_generate.py
```

## Pull Requests

- Keep changes focused.
- Add or update tests when behavior changes.
- Update docs when the public API or workflow changes.
- Do not commit generated assets, local credentials, or cache files.
- Prefer small, reviewable diffs over broad refactors.
