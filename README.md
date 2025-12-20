# filter-openai-plugin

OpenAI filter plugin for photobooth-app.

## Development Setup

1. **Install the main photobooth-app** (either locally or via git):
   ```bash
   pip install -e /path/to/photobooth-app
   ```

2. **Install this plugin in development mode**:
   ```bash
   pip install -e .
   ```

3. **Symlink for local testing** (optional):
   ```bash
   # From your photobooth-app root
   ln -s /path/to/filter-openai-plugin/src/filter_openai plugins/filter_openai
   ```

## Testing

Run tests with:
```bash
pytest
```

## Structure

- `src/filter_openai/` — Plugin source code
- `tests/` — Unit tests
- `pyproject.toml` — Project configuration

## Usage

This plugin provides AI-powered image filters using OpenAI's image generation models.
Configure your OpenAI API key and customize style prompts through the plugin configuration.