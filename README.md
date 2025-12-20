# Plugins for the photobooth-app
This repo contains plugins for the [photobooth-app](https://github.com/photobooth-app/photobooth-app). 

## filter-openai-plugin

OpenAI filter plugin for photobooth-app.

### Features

- **Multiple Models**: Support for gpt-image-1, gpt-image-1-mini, and gpt-image-1.5 (I couldn't get DALL-E2 to work correctly, but I'm leaving it in as a selectable model)
- **Custom style prompts**: The default prompts can be changed or new prompts added by the user.
- **Configurable Parameters**: Adjustable image quality, size, and generation parameters
- **Caching**: Optional result caching to avoid regenerating identical images (useful for switching between styles)
- **Fallback Support**: Option to return original image if AI generation fails

### Missing features
- **Preview Mode**: Currently just returns original image for quick previews, perhaps adding the option to define a "sample" image that is presented as an example for the prompt might be a good workaround; unsure if this can be done via plugins...


## Installation of plugins

The plugins are automatically discovered by the photobooth-app plugin system
when placed in the `plugins/` root directory of the photobooth-app.
See official docs: https://photobooth-app.org/reference/plugins/


## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   # Install runtime dependencies
   uv sync
   
   # Install dev dependencies (includes photobooth-app for testing)
   uv sync --group dev
   ```

3. **Set up local photobooth-app**:
   The dev dependencies include `photobooth-app` configured to install from PyPI.
   To test manually, simpy run `uv run photobooth` from the `photobooth-data` directory in the root of this repo (you will need to create it first)

## Testing

The project includes both unit tests and integration tests:

```bash
# Run all tests
cd photobooth-data && uv run python -m pytest ../tests/ -v

# Run only unit tests
cd photobooth-data && uv run python -m pytest ../tests/test_filter_openai.py -v

# Run only integration tests  
cd photobooth-data && uv run python -m pytest ../tests/test_integration.py -v

# Run integration tests specifically
cd photobooth-data && uv run python -m pytest -m integration -v
```

**Note**: Tests must be run from the `photobooth-data` directory so the plugin system can discover the external plugin and store and use configurations from photobooth.

## Structure

- `photobooth-data/plugins/filter_openai/` — Plugin source code
  - `filter_openai.py` — Main plugin implementation  
  - `config.py` — Plugin configuration
  - `models.py` — Pydantic models
- `tests/` — Test suite
  - `test_filter_openai.py` — Unit tests
  - `test_integration.py` — Integration tests with photobooth app
- `pyproject.toml` — Project configuration with dev dependencies
- `photobooth-data/` — Test environment mimicking photobooth app structure

