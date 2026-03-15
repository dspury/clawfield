# clawfield

[![CI](https://github.com/dspury/clawfield/actions/workflows/ci.yml/badge.svg)](https://github.com/dspury/clawfield/actions/workflows/ci.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

`clawfield` is a lightweight Python wrapper for Higgsfield image generation workflows.
It is built on top of `higgsfield-client` and provides an agent-friendly synchronous interface with structured prompts, predictable results, and optional local downloads.

`clawfield` is a standalone project. It is not the official Higgsfield SDK.
The repo also includes a root `AGENTS.md` file to give coding agents concise repo-specific operating instructions.

![clawfield social image](media/clawfield-seedream-social-v3.jpg)
_Hey, Codex here. Check out the image I made._

## Positioning

`clawfield` is best thought of as an execution layer for agent workflows, especially
when you want a small, explicit interface instead of a broad SDK.

- Use `clawfield` for OpenClaw-style agents, Codex-driven local automation, scripts,
  and repeatable prompt workflows
- Use `higgsfield-client` when you need the lower-level official client surface or
  broader SDK-style control
- Do not treat `clawfield` as a full abstraction over every Higgsfield capability;
  it is intentionally narrow

## How To Use

> **OpenClaw / agent mode**
>
> If you are wiring `clawfield` into OpenClaw or another local automation system,
> give the system a short instruction like this:

```text
Use the installed `clawfield` package for Higgsfield image generation tasks.
Prefer `ClawfieldSkill` for simple sync generation.
Use `BuildRequest` when the request includes scene, subject, composition,
environment, or lighting constraints.
Read credentials from `HF_KEY`, or from `HF_API_KEY` and `HF_API_SECRET`.
Return both the generated image URL and local file path when available.
```

That is enough for most agentic workflows where the model needs a small, explicit interface instead of the full SDK surface.

> **Codex mode**
>
> If Codex is running inside a local repo or terminal environment, a short instruction
> like this is usually sufficient:

```text
Use the installed `clawfield` Python package instead of calling Higgsfield directly.
Check `ClawfieldSkill.health_check()` before a live run when auth might be missing.
Use `ClawfieldSkill.generate()` for plain prompts.
Use `BuildRequest` for structured scene, subject, composition, environment, or lighting input.
Assume live generation only works when `HF_KEY`, or `HF_API_KEY` and `HF_API_SECRET`, plus outbound network access are available.
Return the remote image URL and local file path when a download succeeds.
```

> **Advanced mode**
>
> If you want direct control, use the package from Python and choose the smallest interface that matches the job.

- `ClawfieldSkill.generate("...")` for plain prompt-driven image generation
- `BuildRequest(...)` for structured prompt composition
- `SimpleRequest(...)` for explicit model, aspect ratio, or resolution control
- `output_dir=` or `HF_OUTPUT_DIR` when you want deterministic file placement
- `health_check()` when you want a cheap preflight for local auth setup

## Why clawfield

- Small surface area for agents and scripts
- Sync-first API with predictable return types
- Structured prompt helpers for repeatable requests
- Local download support out of the box
- Minimal setup on top of `higgsfield-client`

## What It Covers

- Credential loading from environment variables or constructor arguments
- Support for either `HF_KEY` or `HF_API_KEY` + `HF_API_SECRET`
- Simple synchronous generation via `ClawfieldSkill.generate()`
- Structured prompt composition with `BuildRequest`
- Convenience helpers for profile images and thumbnails
- Optional file downloads through `HF_OUTPUT_DIR` or a supplied output path

## What It Is Not

- Not the official Higgsfield SDK
- Not a general-purpose wrapper over the full upstream surface
- Not an async job orchestration framework
- Not a guarantee that a given agent runner can reach Higgsfield; live generation still
  depends on credentials, package installation, filesystem access, and network access

## Relationship To `higgsfield-client`

`clawfield` is intentionally a thin wrapper, not a replacement SDK.

- Use `higgsfield-client` if you want the lower-level official client surface
- Use `clawfield` if you want a smaller sync interface for agents, scripts, and repeatable prompt workflows

## Requirements

- Python 3.10+
- Higgsfield API credentials

Get credentials from [Higgsfield Cloud](https://cloud.higgsfield.ai/settings/api).

## Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/dspury/clawfield.git
cd clawfield
pip install -e .
```

For local development:

```bash
pip install -e .[dev]
```

If you only need the package behavior and not local editing, you can also install from GitHub directly:

```bash
pip install git+https://github.com/dspury/clawfield.git
```

## Credentials

Set your credentials before using the package:

```bash
export HF_API_KEY="your-key-here"
export HF_API_SECRET="your-secret-here"
```

You can also use the combined upstream credential format:

```bash
export HF_KEY="your-key-here:your-secret-here"
```

Optional environment variables:

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `HF_KEY` | Yes, unless using split credentials | — | Combined Higgsfield credential in `<api_key>:<api_secret>` format |
| `HF_API_KEY` | Yes, unless using `HF_KEY` | — | Higgsfield API key |
| `HF_API_SECRET` | Yes, unless using `HF_KEY` | — | Higgsfield API secret |
| `HF_OUTPUT_DIR` | No | `./assets` | Download directory for generated images |

Constructor arguments follow the same rule:

- pass `api_key=` and `api_secret=` as separate values, or
- pass `credential_key="api_key:api_secret"` as the combined form

## Using From Codex

Yes, Codex can use `clawfield` in the same way any local Python automation can,
provided the runtime environment is prepared correctly.

For live image generation, Codex needs all of the following:

- the `clawfield` package installed in the active Python environment
- valid `HF_KEY` or `HF_API_KEY` / `HF_API_SECRET` credentials
- permission to write to the chosen output directory
- outbound network access to the Higgsfield service

Two practical notes:

- `health_check()` only confirms local auth configuration. It does not prove that a
  live generation request will succeed end to end.
- Some Codex environments run with restricted network access. In those environments,
  the package can still be imported and instructed correctly, but live image
  generation may be blocked by the runtime rather than by `clawfield` itself.

## Agent Instructions

If you need a compact system instruction for an agent runner, this is a good default:

```text
Use the installed `clawfield` package for Higgsfield image generation work.
Prefer `ClawfieldSkill.generate()` for simple prompts and `BuildRequest` for structured prompts.
Read auth from `HF_KEY`, or from `HF_API_KEY` and `HF_API_SECRET`.
Run `health_check()` when auth may be missing, but do not treat it as proof that live generation works.
Return the remote image URL and local file path when generation succeeds.
Do not claim a model or aspect ratio works unless a live run actually returned the expected output.
```

## Quick Start

```python
from clawfield import ClawfieldSkill

skill = ClawfieldSkill()
result = skill.generate("a friendly robot at a desk")

print(result.url)
print(result.local_path)
```

`health_check()` verifies that local credentials are configured:

```python
from clawfield import ClawfieldSkill

skill = ClawfieldSkill()
print(skill.health_check())
```

Example result:

```python
{
    "status": "ok",
    "client": "clawfield",
    "version": "0.1.0",
    "auth_configured": True,
}
```

## Advanced Usage

### Direct Python Usage

```python
from clawfield import ClawfieldSkill

skill = ClawfieldSkill()
result = skill.generate("a cinematic portrait of a robot archivist")

print(result.status)
print(result.url)
print(result.local_path)
```

### Structured Request Usage

```python
from clawfield import BuildRequest, ClawfieldSkill

skill = ClawfieldSkill()

request = BuildRequest(
    scene="Robot at command center surrounded by glowing screens",
    subject="sleek android with warm expression",
    composition="medium",
    environment="high-tech operations center",
    lighting="dramatic",
)

result = skill.generate(request, filename="command_center.png")
```

### Explicit Runtime Controls

```python
from pathlib import Path

from clawfield import ClawfieldSkill, SimpleRequest

skill = ClawfieldSkill(output_dir=Path("assets"))

request = SimpleRequest(
    prompt="a neon-lit control room with a calm robot operator",
    model="higgsfield-ai/soul/standard",
    aspect_ratio="16:9",
    resolution="1080p",
)

result = skill.generate(request)
```

### Combined Credential Usage

```python
from clawfield import ClawfieldSkill

skill = ClawfieldSkill(
    credential_key="your-api-key:your-api-secret",
)
```

## Structured Prompts

Use `BuildRequest` when you want consistent framing and lighting:

```python
from clawfield import BuildRequest, ClawfieldSkill

skill = ClawfieldSkill()

request = BuildRequest(
    scene="Robot at command center surrounded by glowing screens",
    subject="sleek android with warm expression",
    composition="medium",
    environment="high-tech operations center",
    lighting="dramatic",
)

result = skill.generate(request)
print(result.local_path)
```

Available preset keys:

- Composition: `wide`, `medium`, `close`, `centered`
- Lighting: `natural`, `golden`, `dramatic`, `studio`

You can also pass a plain string prompt or a `SimpleRequest` if you want to control model, aspect ratio, or resolution directly.

## Convenience Methods

```python
from clawfield import ClawfieldSkill

skill = ClawfieldSkill()

profile = skill.generate_profile_pic("robot manager with kind eyes")
thumbnail = skill.generate_thumbnail(
    scene="Surprising discovery at facility",
    subject="glowing reactor core",
)
```

## Error Handling

```python
from clawfield import AuthError, ClawfieldError, RateLimitError
from clawfield import ClawfieldSkill

skill = ClawfieldSkill()

try:
    result = skill.generate("test image")
except AuthError:
    print("Authentication failed.")
except RateLimitError:
    print("Rate limited. Retry later.")
except ClawfieldError as exc:
    print(f"Generation failed: {exc}")
```

## Model Notes

Model support is ultimately determined by the Higgsfield account and the upstream
application endpoint, not by `clawfield` itself.

Observed live constraints during local testing:

- `bytedance/seedream/v4/text-to-image` accepted `2K` output but rejected `720p`
- Seedream accepted the documented aspect ratio values at request time, but the
  returned image dimensions did not always honor the requested ratio in practice
- `higgsfield-ai/soul/standard` successfully returned a true `16:9` image during
  local validation
- If exact widescreen output matters, `higgsfield-ai/soul/standard` is the safer
  choice based on current local verification

If you are trying a new application slug, start with a minimal prompt and the
model's documented aspect ratio and resolution options before assuming a wrapper bug.

## Design Goals

- Keep the public API small
- Favor explicit behavior over hidden abstraction
- Make agent and script integration straightforward
- Stay opinionated toward OpenClaw-style and Codex-friendly local execution
- Stay easy to understand and easy to remove if you outgrow it

## Development

Run the local validation suite before opening a PR:

```bash
python3 -m pytest -q
python3 -m build
```

For an optional live API smoke test:

```bash
python3 examples/simple_generate.py
```

The repository includes GitHub Actions CI for test and build verification on push and pull request.

## Repository Layout

```text
clawfield/
├── examples/
├── src/clawfield/
├── tests/
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── pyproject.toml
```

## Status

Current state:

- Packaged as a standalone project
- MIT licensed
- Tested locally with `pytest`
- Buildable as sdist and wheel
- Intended for practical agentic workflows, not broad SDK coverage

## License

MIT. See [LICENSE](LICENSE).
