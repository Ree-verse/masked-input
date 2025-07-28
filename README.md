<h1 align="center"><code>masked-input</code> - Cross-Platform Password Input with Various Masking Options</h1>

<p align="center">
  <img src="https://raw.githubusercontent.com/ree-verse/masked-input/main/assets/masked-input.svg" alt="masked-input logo" width="350">
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#why-use-masked-input">Why use <code>masked-input</code>?</a> •
  <a href="#features">Features</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#parameters">Parameters</a> •
  <a href="#return-value">Return Value</a> •
  <a href="#exceptions">Exceptions</a> •
  <a href="#implementation-details">Implementation Details</a> •
  <a href="#notes">Notes</a> •
  <a href="#known-issues-and-limitations">Known Issues and Limitations</a> •
  <a href="#examples">Examples</a> •
  <a href="#credits--inspiration">Credits & Inspiration</a> •
  <a href="#license">License</a> •
  <a href="#star-history">Star History</a>
</p>

<div align="center">

[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ree-verse/masked-input)](https://github.com/ree-verse/masked-input/commits)
[![GitHub Issues](https://img.shields.io/github/issues/ree-verse/masked-input.svg?style=flat-square&label=Issues&color=d77982)](https://github.com/ree-verse/masked-input/issues)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/ree-verse/masked-input/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/1262386017202212996?color=738adb&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/ZZfqH9Z4uQ)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/masked-input)](https://pypi.org/project/masked-input)
[![PyPI Status](https://badge.fury.io/py/masked-input.svg)](https://badge.fury.io/py/masked-input)
[![PyPI - Downloads](https://static.pepy.tech/badge/masked-input)](https://pepy.tech/projects/masked-input)

</div>

---

## Overview

The `masked-input` function provides **a secure way to read passwords** or other sensitive input from the command line with **customizable masking**. It works across **different operating systems** and **handles various edge cases**.

## Why Use `masked-input`?

Unlike `getpass`, `masked-input` provides **visual feedback through masking**, improving UX during password entry, especially in CLI tools. It also offers **full customization** and **graceful fallback behavior**.

## Features

- 🌐 **Cross-platform compatibility** - Works on Windows and POSIX-based systems
- 🎭 **Customizable masking character** - Define your own character to mask input (like *, •, or nothing at all)
- 🔢 **Adjustable mask repeat count** - Control how many masking characters appear per typed character, from single to multiple symbols, or even none
- ⌫ **Proper handling of backspace and special keys** - Properly deletes characters and gracefully skips over arrow keys, escape sequences, and other exotic key combos without breaking the mask flow
- ⏱️ **Per-character delay** - Optionally pauses after each typed character
- ⌛ **Global input timeout** - Abort password input after a defined total duration and optionally show a custom message when time runs out
- 🔐 **Character limit** - Define a maximum password length
- 🧭 **Selectable input mode** - Choose between:
  - **standard**: masks each char normally
  - **last-char-temporary**: briefly shows the last char before masking
  - **invisible**: shows nothing at all
  - **pixel-lock**: masks then deletes instantly
- 🧪 **Fallback to standard `getpass` when necessary** - Automatically switches to `getpass` when masking isn’t feasible
- ✍️ **Clear and concise docstrings** - Parameters documented with no fluff, easy to read and maintain
- ✅ **Built-in unit tests** - Comes with a robust suite of unit tests covering key usage scenarios to ensure reliability

## Prerequisites

- **Python 3.9** or higher
- **No external dependencies** (uses only standard library modules)
- **Terminal or command-line environment** that supports interactive input
- On Windows: **A terminal that supports ANSI escape sequences** for best results
- On POSIX: **Terminal with standard TTY capabilities**

## Installation

### Option 1: PyPI

```bash
pip install masked-input
```

### Option 2: Manual Installation

Clone the repository or download the source code, then navigate to the project directory:

```bash
git clone https://github.com/ree-verse/masked-input.git
cd path/to/your/folder
pip install .
```

## Usage

```python
from masked_input import masked_input

# Basic usage with default settings
password = masked_input()  # Displays "Password: " with "•" masking

# Custom prompt, mask character, and mask repeat count
password = masked_input(
    prompt="Enter secret key: ",
    mask="*",
    mask_repeat=2
)

# Hide input completely (no masking character)
password = masked_input(mask="")
```

## API Reference

```python
masked_input(
    prompt: str = 'Password: ',
    mask: str = '•',
    mask_repeat: int = 1,
    char_timeout: Optional[Union[int, float]] = None,
    timeout: Optional[Union[int, float]] = None,
    timeout_prompt: Optional[str] = None,
    char_limit: Optional[int] = None,
    mode: Literal['standard', 'last-char-temporary', 'invisible', 'pixel-lock'] = 'standard',
    last_char_visible_duration: Union[int, float] = 0.1
) -> str
```

## Parameters

| Parameter                    | Type                   | Default        | Description                                                                              |
| ---------------------------- | ---------------------- | -------------- | ---------------------------------------------------------------------------------------- |
| `prompt`                     | `str`                  | `'Password: '` | The text displayed to prompt the user for input                                          |
| `mask`                       | `str`                  | `'•'`          | Character used to mask each input character (use empty string to hide completely)        |
| `mask_repeat`                | `int`                  | `1`            | Number of mask symbols displayed per each input character (1-100)                        |
| `char_timeout`               | `int`, `float`, `None` | `None`         | Delay in seconds after each character input                                              |
| `timeout`                    | `int`, `float`, `None` | `None`         | Total timeout in seconds for the whole input                                             |
| `timeout_prompt`             | `str`, `None`          | `None`         | Message displayed on timeout; requires timeout to be set                                 |
| `char_limit`                 | `int`, `None`          | `None`         | Maximum number of input characters allowed                                               |
| `mode`                       | `str`                  | `'standard'`   | Input display mode with various options [^*]                                             |
| `last_char_visible_duration` | `int`, `float`         | `0.1`          | Duration in seconds the last typed character is visible (only for `last-char-temporary`) |

[^*]
- `'standard'`: Shows mask character for each typed character
- `'last-char-temporary'`: Briefly shows each character before masking it
- `'invisible'`: No visual feedback (no mask, no cursor movement)
- `'pixel-lock'`: No cursor movement to prevent revealing input length

## Return Value

The function returns a string containing the user's input without the masking.

## Exceptions

- `TypeError`:
  - Raised:
    - If `prompt` or `mask` are not strings
    - If `mask_repeat` is not an integer
    - If `char_timeout`, `timeout`, or `last_char_visible_duration` are not int or float
    - If `timeout_prompt` is not a string
    - If `char_limit` is not an integer
    - If `mode` is not a string

- `ValueError`:
  - Raised:
    - If `mask` contains more than one character
    - If `mask` is an empty string but `mode` is not `invisible`
    - If `mask` is not one of `''` or `'•'` when mode is `invisible`
    - If `mask_repeat` is not between 1 and 100
    - If `timeout_prompt` is provided without setting `timeout`
    - If `timeout_prompt` is an empty string
    - If `char_limit` is set but not positive
    - If `mode` is not one of: `standard`, `last-char-temporary`, `invisible`, `pixel-lock`
    - If `mode` is `invisible` or `mask` is empty and `mask_repeat`, `char_timeout`, or `last_char_visible_duration` are set to non-default values
    - If `last_char_visible_duration` is set while `mode` is not `last-char-temporary`
    - If `last_char_visible_duration` is not greater than zero

- `KeyboardInterrupt`:
  - Raised:
    - If the user interrupts input (e.g., by pressing Ctrl+C)

## Implementation Details

- On Windows systems, the function uses the `msvcrt` module to read characters
- On POSIX-based systems, it uses `termios` and `tty` to set the terminal to raw mode
- Falls back to `getpass` when the script is not run in an interactive terminal

## Notes

- Special keys (arrows, function keys, etc.) are properly handled and ignored
- The function correctly processes backspace to remove the last character
- Only printable characters are added to the password
- The terminal is restored to its original state even if an exception occurs
- The `mask_repeat` parameter must be an integer between 1 and 100 to avoid overflow errors or memory issues during mask repetition. Values outside this range may raise an `OverflowError` or `MemoryError`

## Known Issues and Limitations

- Windows Character Input: On Windows systems, certain characters like "à" and other accented characters require pressing the key twice to be registered correctly. This is due to how the Windows console handles special characters.
- Very long passwords may cause display issues in terminals with limited width. This does not affect password entry itself, only its visual representation.
- On Windows and POSIX, `Ctrl+M` and `Ctrl+J` send the same sequences as `Enter` (`\r`) and `Line Feed` (`\n`), so they behave like pressing Enter. Similarly, `Ctrl+H` sends the same sequence as Backspace (`\b`), which deletes a character. Since `masked-input` focuses on handling individual key inputs (not complex shortcuts), these overlaps are expected and not treated specially just like in `getpass` and Python’s standard `input`.
- Input with non-standard keyboard layouts may have unexpected behavior on some platforms.
- Some terminal emulators may not properly handle the masking behavior, especially when using uncommon terminal settings.
- No error is raised if `last_char_visible_duration` is set while mode isn’t `last-char-temporary`, as long as its value remains at 0.1 (the default).

## Examples

```python
# Standard masking:
password = masked_input(prompt="Enter password: ", mask="*")

# Temporarily showing each character before masking:
password = masked_input(
    prompt="Enter password: ",
    mask="*",
    mode="last-char-temporary",
    last_char_visible_duration=0.2
)

# Invisible input (no visual feedback):
password = masked_input(mode="invisible")

# Input with timeout:
password = masked_input(
    timeout=30,
    timeout_prompt="Input timed out!"
)

# Character limit:
password = masked_input(char_limit=12)

# Delay between each character input (slows down rendering intentionally):
password = masked_input(
    prompt="Password: ",
    char_timeout=0.3
)

# Mask repeated for each character (e.g., "**" instead of "*"):
password = masked_input(
    mask ="*",
    mask_repeat=2
)
```

```python
# Example usage:
password = masked_input(prompt='Enter your password: ', mask='*', mask_repeat=2)
print(f'Your password is: {password}')
```

## Credits & Inspiration

This project was inspired by [pwinput](https://github.com/asweigart/pwinput), which provided the initial idea and implementation of cross-platform masked input in Python.

Big respect to Al Sweigart for his contributions to the open-source ecosystem.

## License

Released under the [MIT License](https://github.com/Ree-verse/masked-input/blob/main/LICENSE) © 2025 [Ree-verse](https://github.com/ree-verse).

## Star History

<a href="https://star-history.com/#Ree-verse/masked-input&Timeline">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Ree-verse/masked-input&type=Timeline&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Ree-verse/masked-input&type=Timeline" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Ree-verse/masked-input&type=Timeline" />
  </picture>
</a>

Disclaimer: This program may contain bugs. It has only been tested on AZERTY keyboards and may not function correctly on QWERTY layouts. If you encounter any issues, please open an issue to report them.
