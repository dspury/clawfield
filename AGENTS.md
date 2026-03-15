# AGENTS

Purpose: repo-local instructions for coding agents working on `clawfield`.

- Keep `clawfield` narrow: it is a thin execution layer, not a full Higgsfield SDK.
- Prefer `ClawfieldSkill.generate()` for simple runs and `BuildRequest` for structured prompts.
- Accept auth via `HF_KEY` or `HF_API_KEY` + `HF_API_SECRET`.
- Do not claim live model, aspect ratio, or API behavior unless you actually ran it.
- Validate with `python3 -m pytest -q` and `python3 -m build` when code changes.
