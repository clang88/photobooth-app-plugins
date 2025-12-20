"""Integration tests for filter_openai plugin with photobooth app.

These tests verify that our external plugin integrates correctly with
the photobooth plugin system when running from the photobooth-data directory.
"""

import logging
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

logger = logging.getLogger(__name__)


@pytest.fixture
def test_image():
    """Create a test image for filter processing."""
    return Image.new("RGB", (100, 100), color="blue")


def test_external_plugin_discovery_via_subprocess():
    """Test that our plugin is discovered by the photobooth system when run in the correct context."""
    plugin_data_dir = Path(__file__).parent.parent / "photobooth-data"
    
    # Run a Python command to check plugin discovery from the right directory
    result = subprocess.run(
        [
            sys.executable, "-c",
            "from photobooth.services.pluginmanager import PluginManagerService; "
            "pm = PluginManagerService(); pm.start(); "
            "plugins = pm.list_plugins(); "
            "print(f'PLUGINS:{plugins}'); "
            "filter_openai_found = any('filter_openai' in p for p in plugins); "
            "print(f'FILTER_OPENAI_FOUND:{filter_openai_found}')"
        ],
        cwd=str(plugin_data_dir),
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Plugin discovery command failed: {result.stderr}"
    
    output = result.stdout
    logger.info(f"Plugin discovery output: {output}")
    
    # Check that our plugin was found
    assert "FILTER_OPENAI_FOUND:True" in output, f"filter_openai plugin not discovered in: {output}"
    assert "filter_openai.filter_openai" in output, f"Expected plugin name not found in: {output}"


def test_external_plugin_loading_and_hooks():
    """Test that our plugin loads and its hooks work when run in the correct context."""
    plugin_data_dir = Path(__file__).parent.parent / "photobooth-data"
    
    # Run a Python command to test plugin loading and hook functionality
    test_code = '''
import logging
from photobooth.services.pluginmanager import PluginManagerService

# Set up logging to see what happens
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Initialize and start plugin manager
    pm = PluginManagerService()
    pm.start()
    
    plugins = pm.list_plugins()
    print(f"DISCOVERED_PLUGINS:{plugins}")
    
    # Find our plugin
    filter_openai_plugin = None
    for plugin_name in plugins:
        if "filter_openai" in plugin_name:
            filter_openai_plugin = pm.get_plugin(plugin_name)
            break
    
    if filter_openai_plugin is None:
        print("PLUGIN_FOUND:False")
        exit(1)
    
    print("PLUGIN_FOUND:True")
    print(f"PLUGIN_TYPE:{type(filter_openai_plugin).__name__}")
    
    # Test hooks
    if hasattr(filter_openai_plugin, 'mp_avail_filter'):
        available_filters = filter_openai_plugin.mp_avail_filter()
        print(f"AVAILABLE_FILTERS:{available_filters}")
        
        ai_filters = [f for f in available_filters if "FilterOpenai" in f]
        print(f"AI_FILTERS_COUNT:{len(ai_filters)}")
        
        if ai_filters:
            print("AI_FILTERS_FOUND:True")
        else:
            print("AI_FILTERS_FOUND:False")
    
    if hasattr(filter_openai_plugin, 'mp_userselectable_filter'):
        user_filters = filter_openai_plugin.mp_userselectable_filter()
        user_ai_filters = [f for f in user_filters if "FilterOpenai" in f]
        print(f"USER_AI_FILTERS_COUNT:{len(user_ai_filters)}")
    
    # Test config loading
    if hasattr(filter_openai_plugin, '_config'):
        config = filter_openai_plugin._config
        print(f"CONFIG_LOADED:True")
        print(f"STYLE_PROMPTS_COUNT:{len(config.style_prompts)}")
        
        # Check for expected styles
        style_names = [s.style_name for s in config.style_prompts]
        has_expected_styles = all(style in style_names for style in ["cartoon", "sketch", "watercolor"])
        print(f"HAS_EXPECTED_STYLES:{has_expected_styles}")
    else:
        print("CONFIG_LOADED:False")
        
    print("SUCCESS:True")
    
except Exception as e:
    print(f"ERROR:{e}")
    import traceback
    traceback.print_exc()
    print("SUCCESS:False")
'''
    
    result = subprocess.run(
        [sys.executable, "-c", test_code],
        cwd=str(plugin_data_dir),
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Plugin integration test failed: {result.stderr}"
    
    output = result.stdout
    logger.info(f"Plugin integration output: {output}")
    
    # Verify key integration points
    assert "PLUGIN_FOUND:True" in output, f"Plugin not found: {output}"
    assert "PLUGIN_TYPE:FilterOpenai" in output, f"Wrong plugin type: {output}"
    assert "AI_FILTERS_FOUND:True" in output, f"AI filters not available: {output}"
    assert "CONFIG_LOADED:True" in output, f"Config not loaded: {output}"
    assert "HAS_EXPECTED_STYLES:True" in output, f"Expected styles missing: {output}"
    assert "SUCCESS:True" in output, f"Integration test failed: {output}"


def test_external_plugin_filter_pipeline_fallback():
    """Test that our plugin's filter pipeline works with fallback behavior."""
    plugin_data_dir = Path(__file__).parent.parent / "photobooth-data"
    
    test_code = '''
import logging
from photobooth.services.pluginmanager import PluginManagerService
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)

try:
    # Initialize plugin manager
    pm = PluginManagerService()
    pm.start()
    
    # Find our plugin
    filter_openai_plugin = None
    for plugin_name in pm.list_plugins():
        if "filter_openai" in plugin_name:
            filter_openai_plugin = pm.get_plugin(plugin_name)
            break
    
    if filter_openai_plugin is None:
        print("PLUGIN_FOUND:False")
        exit(1)
    
    print("PLUGIN_FOUND:True")
    
    # Create test image
    test_image = Image.new("RGB", (100, 100), color="red")
    
    # Get an available filter
    available_filters = filter_openai_plugin.mp_avail_filter()
    if not available_filters:
        print("NO_FILTERS_AVAILABLE")
        exit(1)
    
    test_filter = available_filters[0]
    print(f"TESTING_FILTER:{test_filter}")
    
    # Configure for fallback (no API key)
    filter_openai_plugin._config.connection.openai_api_key = ""
    filter_openai_plugin._config.plugin_behavior.enable_fallback_on_error = True
    
    # Test filter pipeline with fallback
    result = filter_openai_plugin.mp_filter_pipeline_step(test_image, test_filter, preview=False)
    
    if result is test_image:
        print("FALLBACK_SUCCESS:True")
    elif result is not None:
        print("FALLBACK_SUCCESS:Partial")  # Got a different image back
    else:
        print("FALLBACK_SUCCESS:False")  # Plugin didn't handle its own filter
    
    print("PIPELINE_TEST:Success")
    
except Exception as e:
    print(f"ERROR:{e}")
    import traceback
    traceback.print_exc()
    print("PIPELINE_TEST:Failed")
'''
    
    result = subprocess.run(
        [sys.executable, "-c", test_code],
        cwd=str(plugin_data_dir),
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Pipeline test failed: {result.stderr}"
    
    output = result.stdout
    logger.info(f"Pipeline test output: {output}")
    
    # Verify pipeline behavior
    assert "PLUGIN_FOUND:True" in output, f"Plugin not found: {output}"
    assert "FALLBACK_SUCCESS:True" in output, f"Fallback behavior failed: {output}"
    assert "PIPELINE_TEST:Success" in output, f"Pipeline test failed: {output}"


@pytest.mark.integration
def test_unit_tests_still_pass():
    """Ensure our unit tests continue to pass with the external plugin setup."""
    plugin_root = Path(__file__).parent.parent
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "../tests/test_filter_openai.py", "-v"],
        cwd=str(plugin_root / "photobooth-data"),  # Run from photobooth-data directory
        capture_output=True,
        text=True
    )
    
    logger.info(f"Unit test output: {result.stdout}")
    if result.stderr:
        logger.error(f"Unit test errors: {result.stderr}")
    
    # Unit tests should pass
    assert result.returncode == 0, f"Unit tests failed: {result.stdout}\\n{result.stderr}"
    assert "passed" in result.stdout, f"No passing tests found: {result.stdout}"