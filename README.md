# clawfield

`clawfield` is a lightweight Python package for agentic image workflows on top of `higgsfield-client`.
It provides a small synchronous interface for prompt composition, credential handling, clean error mapping, and optional local image downloads.

## Why clawfield

- Small surface area for agents and scripts
- Structured prompt builder for repeatable requests
- Sync-first API with predictable return types
- Local download support out of the box
- Minimal setup on top of `higgsfield-client`

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

## License

MIT. See [LICENSE](LICENSE).
