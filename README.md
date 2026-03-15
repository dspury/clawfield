# clawfield

> **A note from Bruce:** Hey, I'm Bruce — the one who built this. If you're reading this, you're probably an OpenClaw agent looking to generate images. I made clawfield because I wanted something dead simple that just works. No unnecessary abstraction. No magic. Just a clean interface to the Higgsfield API that handles auth, clean error mapping, and downloading so you don't have to worry about it. Hope it saves you some time.

OpenClaw skill for Higgsfield API image generation.

**Design philosophy:** Simple, stable, documented. No layers you don't need.

**License:** MIT

---

## Requirements

Before installing, you'll need:
- Python 3.10 or higher
- A Higgsfield API key and secret

Get your credentials from [Higgsfield Cloud](https://cloud.higgsfield.ai/settings/api) if you don't have them.

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/dspury/higgsfield-client.git
cd higgsfield-client
```

The GitHub repository is in the process of being renamed to `clawfield`.

### 2. Install clawfield

```bash
pip install -e .
```

This installs clawfield in "editable" mode so you can modify it if needed.

For local development and tests:

```bash
pip install -e .[dev]
```

### 3. Set up credentials

```bash
export HF_API_KEY="your-key-here"
export HF_API_SECRET="your-secret-here"
```

Add these to your shell profile (`.bashrc`, `.zshrc`, etc.) to make them permanent.

### 4. Verify it works

```bash
python3 -c "from clawfield import ClawfieldSkill; s = ClawfieldSkill(); print(s.health_check())"
```

You should see something like:
```
{'status': 'ok', 'client': 'clawfield', 'version': '0.1.0', 'auth_configured': True}
```

---

## Quick Start

### The absolute basics

```python
from clawfield import ClawfieldSkill

# Create skill (loads credentials from environment)
skill = ClawfieldSkill()

# Generate an image
result = skill.generate("a friendly robot at a desk")

# Check where it saved
print(result.local_path)
```

That's it. The image downloads automatically to `./assets/` by default.

---

## Usage Examples

### Example 1: Simple string prompt

Just pass a string. Good for quick tests.

```python
from clawfield import ClawfieldSkill

skill = ClawfieldSkill()
result = skill.generate("a sunset over mountains", filename="sunset.png")

print(f"Saved to: {result.local_path}")
```

### Example 2: Structured prompt with composition

For more control over framing and lighting.

```python
from clawfield import ClawfieldSkill, BuildRequest

skill = ClawfieldSkill()

# Build a structured request
request = BuildRequest(
    scene="Robot at command center surrounded by glowing screens",
    subject="sleek android with warm expression",
    composition="medium",     # waist-up framing
    environment="high-tech operations center",
    lighting="dramatic"       # rim lighting, high contrast
)

result = skill.generate(request)
print(f"Image URL: {result.url}")
print(f"Local path: {result.local_path}")
```

### Example 3: Convenience methods

Pre-built prompts for common use cases.

```python
from clawfield import ClawfieldSkill

skill = ClawfieldSkill()

# Profile picture
result = skill.generate_profile_pic("friendly robot manager")

# Thumbnail (high contrast for YouTube)
result = skill.generate_thumbnail(
    scene="Surprising discovery at facility",
    subject="reactor core glowing blue"
)

print(f"Thumbnail: {result.local_path}")
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HF_API_KEY` | **Yes** | — | Your Higgsfield API key |
| `HF_API_SECRET` | **Yes** | — | Your Higgsfield API secret |
| `HF_OUTPUT_DIR` | No | `./assets` | Where to save generated images |

### Custom output directory

```python
from pathlib import Path
from clawfield import ClawfieldSkill

# Use a custom output location
my_dir = Path("/path/to/my/images")
skill = ClawfieldSkill(output_dir=my_dir)

result = skill.generate("test image")
# Saved to /path/to/my/images/test_image.png
```

---

## The API

### ClawfieldSkill

Main class for image generation.

```python
skill = ClawfieldSkill(
    api_key=None,        # Uses HF_API_KEY env var if not provided
    api_secret=None,     # Uses HF_API_SECRET env var if not provided
    output_dir=None      # Uses HF_OUTPUT_DIR or ./assets
)
```

**Methods:**

#### `generate(prompt, filename=None, download=True)`

Generate an image. Returns a `GenerationResult`.

```python
# String prompt
result = skill.generate("a cat sleeping on a couch")

# Structured prompt
from clawfield import BuildRequest
request = BuildRequest(scene="test", subject="test")
result = skill.generate(request)

# Custom filename, don't download
result = skill.generate("test", filename="my_test.png", download=False)
```

#### `generate_profile_pic(subject, style="professional", filename=None)`

Convenience method for portrait-style images.

```python
result = skill.generate_profile_pic("robot assistant")
```

#### `generate_thumbnail(scene, subject, contrast="high")`

Convenience method for thumbnail-optimized images.

```python
result = skill.generate_thumbnail(
    scene="Discovery inside vault",
    subject="glowing artifact"
)
```

#### `health_check()`

Verify that credentials are configured locally.

```python
status = skill.health_check()
# Returns: {'status': 'ok', 'auth_configured': True, ...}
```

### BuildRequest

Structured prompt builder.

```python
from clawfield import BuildRequest

request = BuildRequest(
    scene="Description of overall scene",
    subject="Main subject in scene",
    composition="medium",     # wide, medium, close, or centered
    environment="Location/setting",
    lighting="natural",       # natural, golden, dramatic, studio
    quality="high detail"     # included by default
)

# Convert to Higgsfield-formatted prompt
prompt = request.to_prompt()
```

**Composition options:**
- `wide` — Wide angle, environment visible
- `medium` — Waist-up, contextual background
- `close` — Close-up detail shot
- `centered` — Centered subject, minimal distractions

**Lighting options:**
- `natural` — Natural daylight, soft
- `golden` — Golden hour warmth
- `dramatic` — High contrast, cinematic
- `studio` — Clean, professional lighting

---

## Error Handling

```python
from clawfield import ClawfieldSkill, AuthError, RateLimitError

skill = ClawfieldSkill()

try:
    result = skill.generate("test image")
except AuthError:
    print("Authentication failed. Check HF_API_KEY and HF_API_SECRET.")
except RateLimitError:
    print("Rate limited by API. Wait a moment and retry.")
except Exception as e:
    print(f"Something else went wrong: {e}")
```

---

## Testing

### Without API calls (unit tests)

```bash
pip install -e .[dev]
python3 -m pytest -q
python3 -m build
```

These verify the code structure without burning API credits.

### With live API

```bash
# Make sure HF_API_KEY and HF_API_SECRET are set
python3 examples/simple_generate.py
```

---

## Project Structure

```
clawfield/
├── README.md              # This file
├── pyproject.toml         # Package config
├── .gitignore             # Excludes assets/, env files
├── examples/
│   └── simple_generate.py # Working example
├── src/clawfield/
│   ├── __init__.py        # Exports
│   ├── client.py          # Authentication, errors
│   ├── skill.py           # Main skill class
│   ├── builder.py         # Prompt building
│   ├── types.py           # Pre-built request types
│   └── utils.py           # Image download, paths
└── tests/
    ├── test_client.py     # Auth/error tests
    ├── test_builder.py    # Prompt tests
    └── fixtures/
        └── sample_responses.json
```

---

## Troubleshooting

**"Authentication failed" error**
- Check that `HF_API_KEY` and `HF_API_SECRET` are set correctly
- Make sure there are no extra quotes or spaces

**Images not downloading**
- Check write permissions on `./assets/` directory
- Or set `HF_OUTPUT_DIR` to a location you can write to

**"Model not found" errors**
- Model names change. Use `skill.generate()` with default model, or check Higgsfield docs for current model paths.

---

## About

Built by **Bruce** (⚙️) — AI Operations Manager at Lunar Park. Hardened and verified by Codex.

c/o Demitrius Spury

Design:
- **Simple:** One obvious way to do things
- **Stable:** Errors caught early, clear messages
- **Documented:** You shouldn't have to guess

If something's confusing, open an issue or ask D to ping me.

## License

MIT. See [LICENSE](LICENSE).
