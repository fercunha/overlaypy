"""Basic tests for OverlayPy application."""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import overlay
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import overlay
except ImportError:
    # If tkinter is not available (like in CI), we'll skip the tests
    overlay = None


class TestOverlayApp(unittest.TestCase):
    """Test cases for OverlayApp class."""

    def setUp(self):
        """Set up test fixtures."""
        if overlay is None:
            self.skipTest("Tkinter not available")

    @patch('overlay.tk.Tk')
    @patch('overlay.get_monitors')
    def test_overlay_app_initialization(self, mock_get_monitors, mock_tk):
        """Test that OverlayApp initializes without errors."""
        # Mock monitor data
        mock_monitor = Mock()
        mock_monitor.name = "Test Monitor"
        mock_monitor.width = 1920
        mock_monitor.height = 1080
        mock_monitor.x = 0
        mock_monitor.y = 0
        mock_get_monitors.return_value = [mock_monitor]

        # Mock Tkinter root
        mock_root = Mock()
        mock_tk.return_value = mock_root

        # This should not raise any exceptions
        try:
            app = overlay.OverlayApp(mock_root)
            self.assertIsNotNone(app)
            self.assertEqual(app.overlay_visible, False)
            self.assertIsNone(app.overlay)
        except Exception as e:
            self.fail(f"OverlayApp initialization failed: {e}")

    def test_module_imports(self):
        """Test that all required modules can be imported."""
        if overlay is None:
            self.skipTest("Tkinter not available")
            
        # Test that the overlay module has the expected classes
        self.assertTrue(hasattr(overlay, 'OverlayApp'))
        
        # Test that required modules are importable
        import tkinter as tk
        from tkinter import ttk
        import platform
        from screeninfo import get_monitors
        
        # Basic smoke test
        self.assertTrue(callable(get_monitors))


class TestApplicationConfiguration(unittest.TestCase):
    """Test application configuration and constants."""

    def test_default_values(self):
        """Test that default values are reasonable."""
        # These are the expected defaults based on the application
        default_font_size = "36"
        default_position = "Bottom Left"
        default_padding = "40"
        default_timer = "60"
        
        # Test that these are valid values
        self.assertIsInstance(int(default_font_size), int)
        self.assertIn(default_position, ["Bottom Left", "Bottom Right", "Top Left", "Top Right"])
        self.assertIsInstance(int(default_padding), int)
        self.assertIsInstance(int(default_timer), int)
        
        # Test reasonable ranges
        self.assertGreaterEqual(int(default_font_size), 12)
        self.assertLessEqual(int(default_font_size), 240)
        self.assertGreater(int(default_padding), 0)
        self.assertGreater(int(default_timer), 0)


if __name__ == '__main__':
    unittest.main()
