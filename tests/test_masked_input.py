# =========================================== WARNING: DO NOT USE PYTEST HERE ===========================================
# NOTE: These tests simulate interactive keyboard input using 'keyboard'.
# Pytest captures stdin by default, which blocks real input and causes hangs or errors.
# Therefore, we avoid pytest here and use unittest without output capture to allow keyboard simulation to work properly.
# =======================================================================================================================

import io
import sys
import threading
import time
import unittest

try:
    import keyboard
except ImportError:
    keyboard = None  # Used to skip tests if 'keyboard' isn't available

from masked_input import masked_input


def _simulate_keyboard_action(action, *args, delay: float = 0.05, **kwargs):
    def worker():
        time.sleep(delay)
        action(*args, **kwargs)

    threading.Thread(target=worker, daemon=True).start()


def simulate_typing(text: str, delay: float = 0.05):
    _simulate_keyboard_action(keyboard.write, text, delay=delay)


def simulate_keys(keys: list[str], text: str, delay: float = 0.05):
    def press_keys_then_write():
        for key in keys:
            keyboard.send(key)
            time.sleep(0.02)
        keyboard.write(text)

    _simulate_keyboard_action(press_keys_then_write, delay=delay)


def simulate_ctrl_c(delay: float = 0.05):
    _simulate_keyboard_action(keyboard.press_and_release, "ctrl+c", delay=delay)


@unittest.skipUnless(
    all(hasattr(keyboard, fn) for fn in ['write', 'send', 'press_and_release']),
    "keyboard module not functional or installed"
)
class TestMaskedInput(unittest.TestCase):
    """Unit tests for the masked_input function using simulated keyboard input."""

    def setUp(self):
        self._original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        self.addCleanup(self._restore_stdout)

    def _restore_stdout(self):
        sys.stdout = self._original_stdout  # Restore stdout

    def test_masked_input_empty_password(self):
        simulate_typing("\n")
        result = masked_input(prompt="Enter empty password: ")
        self.assertEqual(result, "")

    def test_masked_input_basic(self):
        test_cases = [
            ("password\n", "password"),
            ("secret\bX\n", "secreX"),
            ("12345\b\b67\n", "12367"),
            ("start\b\b\b\b\bnew\n", "new"),
        ]
        for input_text, expected in test_cases:
            simulate_typing(input_text)
            result = masked_input(prompt="Test: ")
            self.assertEqual(result, expected)

    def test_masked_input_overkill_backspace(self):
        simulate_typing("abc" + ("\b" * 10) + "xyz\n")
        result = masked_input(prompt="Backspace test: ")
        self.assertEqual(result, "xyz")

    def test_masked_input_full_ascii(self):
        test_string = r"""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=~!@#$%^&*()_+,./;\'<>?:"[]{}"""
        simulate_typing(test_string + "\n")
        result = masked_input(prompt="ASCII test: ")
        self.assertEqual(result, test_string)

    def test_masked_input_multiple_escape_sequences_ignored(self):
        keys = ["up", "down", "left", "right", "delete", "escape", "tab", "ctrl", "alt", "shift", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]
        simulate_keys(keys, "MyPass123\n")
        result = masked_input(prompt="Escape seq test: ")
        self.assertEqual(result, "MyPass123")

    def test_masked_input_keyboard_interrupt(self):
        simulate_ctrl_c()
        with self.assertRaises(KeyboardInterrupt):
            masked_input(prompt="Interrupt test: ")


if __name__ == "__main__":
        unittest.main()
