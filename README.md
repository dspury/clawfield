# clawfield

[![CI](https://github.com/dspury/clawfield/actions/workflows/ci.yml/badge.svg)](https://github.com/dspury/clawfield/actions/workflows/ci.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

`clawfield` is a lightweight Python wrapper for Higgsfield image generation workflows.
It is built on top of `higgsfield-client` and provides an agent-friendly synchronous interface with structured prompts, predictable results, and optional local downloads.

`clawfield` is a standalone project. It is not the official Higgsfield SDK.

## How To Use

> **Easy mode**
>
> If you are wiring `clawfield` into an agent or local automation system, give the system a short instruction like this:

```text
Use the installed `clawfield` package for Higgsfield image generation tasks.
Prefer `ClawfieldSkill` for simple sync generation.
Use `BuildRequest` when the request includes scene, subject, composition,
environment, or lighting constraints.
Read credentials from `HF_API_KEY` and `HF_API_SECRET`.
Return both the generated image URL and local file path when available.
```

That is enough for most agentic workflows where the model needs a small, explicit interface instead of the full SDK surface.

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
- Simple synchronous generation via `ClawfieldSkill.generate()`
- Structured prompt composition with `BuildRequest`
- Convenience helpers for profile images and thumbnails
- Optional file downloads through `HF_OUTPUT_DIR` or a supplied output path

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

Optional environment variables:

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `HF_API_KEY` | Yes | — | Higgsfield API key |
| `HF_API_SECRET` | Yes | — | Higgsfield API secret |
| `HF_OUTPUT_DIR` | No | `./assets` | Download directory for generated images |

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

## Design Goals

- Keep the public API small
- Favor explicit behavior over hidden abstraction
- Make agent and script integration straightforward
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
