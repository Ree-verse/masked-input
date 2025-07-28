"""
masked-input - Cross-platform password input with various masking options.

Author: Ree-verse (GitHub username)
License: MIT - See LICENSE file for details
"""

__all__ = ['masked_input']
__version__ = '1.0.0'
__author__ = 'Ree-verse'
__license__ = 'MIT'
__doc__ = 'Cross-platform library to read password input with various masking options.'

import os
import sys
import time
from typing import Annotated, Literal, Optional, Union


def masked_input(
    prompt: str = 'Password: ',
    mask: str = '•',
    mask_repeat: Annotated[int, range(1, 101)] = 1,
    char_timeout: Optional[Union[int, float]] = None,
    timeout: Optional[Union[int, float]] = None,
    timeout_prompt: Optional[str] = None,
    char_limit: Optional[int] = None,
    mode: Literal['standard', 'last-char-temporary', 'invisible', 'pixel-lock'] = 'standard',
    last_char_visible_duration: Union[int, float] = 0.1
) -> str:
    """
    Reads a masked password from standard input in a cross-platform way.

    Args:
        prompt (str): The prompt message displayed to the user.
        mask (str): The character used to mask input (a single character or empty string).
        mask_repeat (int): Number of times the mask character is repeated per typed character (1-100).
        char_timeout (int, float or None): Delay in seconds after each character input.
        timeout (int, float or None): Total timeout in seconds for the whole input.
        timeout_prompt (str or None): Message displayed on timeout; requires timeout to be set.
        char_limit (int or None): Maximum number of input characters allowed.
        mode (`standard`, `last-char-temporary`, `invisible`, `pixel-lock`): Input display mode.
        last_char_visible_duration (int or float): Duration in seconds the last typed character is visible (only for `last-char-temporary`).

    Raises:
        TypeError:
            - If `prompt` or `mask` are not strings.
            - If `mask_repeat` is not an integer.
            - If `char_timeout`, `timeout`, or `last_char_visible_duration` are not int or float.
            - If `timeout_prompt` is not a string.
            - If `char_limit` is not an integer.
            - If `mode` is not a string.

        ValueError:
            - If `mask` contains more than one character.
            - If `mask` is an empty string but `mode` is not `invisible`.
            - If `mask` is not one of `''` or `'•'` when mode is `invisible`.
            - If `mask_repeat` is not between 1 and 100.
            - If `timeout_prompt` is provided without setting `timeout`.
            - If `timeout_prompt` is an empty string.
            - If `char_limit` is set but not positive.
            - If `mode` is not one of: `standard`, `last-char-temporary`, `invisible`, `pixel-lock`.
            - If `mode` is `invisible` or `mask` is empty and `mask_repeat`, `char_timeout`, or `last_char_visible_duration` are set to non-default values.
            - If `last_char_visible_duration` is set while `mode` is not `last-char-temporary`.
            - If `last_char_visible_duration` is not greater than zero.

        KeyboardInterrupt:
            - If the user interrupts input (e.g., by pressing Ctrl+C).

    Returns:
        str: The password entered by the user.
    """

    if not sys.stdin.isatty():  # Falls back to getpass if input is not from an interactive terminal
        import getpass
        return getpass.getpass(prompt)

    full_type_names = {'int': 'integer', 'str': 'string', 'bool': 'boolean'}

    validations = [
        ('prompt', prompt, str, 'a string', False),
        ('mask', mask, str, 'a string', False),
        ('mask_repeat', mask_repeat, int, 'an integer', False),
        ('char_timeout', char_timeout, (int, float), 'a float or an integer', True),
        ('timeout', timeout, (int, float), 'a float or an integer', True),
        ('timeout_prompt', timeout_prompt, str, 'a string', True),
        ('char_limit', char_limit, int, 'an integer', True),
        ('mode', mode, str, 'a string', False),
        ('last_char_visible_duration', last_char_visible_duration, (int, float), 'a float or an integer', False),
    ]

    for name, value, expected_types, description, optional in validations:
        if not optional or value is not None:
            if not isinstance(value, expected_types):
                actual_type_name = type(value).__name__
                full_actual_type_name = full_type_names.get(actual_type_name, actual_type_name)
                raise TypeError(f'{name} must be {description}, not {full_actual_type_name}')

    if len(mask) > 1:
        raise ValueError('mask must be a single character or empty')
    if mask == '' and mode != 'invisible':
        raise ValueError('if mask is empty, mode must be invisible')
    if mask not in ('', '•') and mode == 'invisible' :
        raise ValueError('mask must be \'\' or \'•\' when mode is invisible')
    if not (1 <= mask_repeat <= 100):
        raise ValueError('mask_repeat must be an integer between 1 and 100')  # Avoids potential 'OverflowError' or 'MemoryError' exceptions
    if timeout is None and timeout_prompt is not None:  # Note: no error is raised if timeout_prompt remains at None (default), even when there isn't timeout
        raise ValueError('timeout_prompt must not be set if timeout is not defined')
    if timeout_prompt == '':
        raise ValueError('timeout_prompt must not be an empty string')
    if char_limit is not None and char_limit <= 0:
        raise ValueError('char_limit must be greater than 0')
    if mode not in (valid_modes := {'standard', 'last-char-temporary', 'invisible', 'pixel-lock'}):
        raise ValueError(f'mode must be one of: {", ".join(valid_modes)}')

    if mode == 'invisible' or mask == '':
        forbidden_params = {
            'mask_repeat': mask_repeat,
            'char_timeout': char_timeout,
            'last_char_visible_duration': last_char_visible_duration
        }

        invalid = [
        name for name, value in forbidden_params.items()
        if value not in (None, 0.1 if name == 'last_char_visible_duration' else 1 if name == 'mask_repeat' else None)  # Same permissive-default logic phenomenon as with timeout_prompt and timeout (see above) but for last_char_visible_duration and mask_repeat
        ]

        if invalid:
            raise ValueError(f'{", ".join(invalid)} must not be set when mode is invisible or mask is empty')

    if mode != 'last-char-temporary' and last_char_visible_duration != 0.1:  # See comment above
        raise ValueError('last_char_visible_duration must only be set if mode is last-char-temporary')
    if mode == 'last-char-temporary' and last_char_visible_duration <= 0:
        raise ValueError('last_char_visible_duration must be greater than 0')

    sys.stdout.write(prompt)  # Required prompt
    sys.stdout.flush()

    password = []

    deadline = time.monotonic() + timeout if timeout is not None else None

    def handle_char_timeout() -> None:
        """Optional delay after each character input."""
        if char_timeout:
            time.sleep(char_timeout)

    def handle_timeout() -> bool:
        """Checks if timeout has been reached and displays timeout_prompt if provided. Returns True if a timeout occurred, False otherwise."""
        if deadline and time.monotonic() > deadline:

            if timeout_prompt:
                sys.stdout.write(f'\n{timeout_prompt}\n')
                sys.stdout.flush()
            return True

        return False

    def skip_escape_sequence() -> None:
        """Skips ANSI escape sequences (e.g., arrow/function keys) to prevent them from being processed as regular input."""

        # Reads and grabs (skips) the first byte after ESC in the escape sequence (usually '[' or 'O')
        # If no character is read, exits early to avoid errors
        if not (next_char := sys.stdin.read(1)):
            return

        # Handles CSI sequences starting with '[' (arrows, F5–F12, etc.)
        if next_char == '[':

            # Consumes the rest of the escape sequence until it ends with a letter or '~', the ANSI escape terminator
            while True:
                if not (current_char := sys.stdin.read(1)) or current_char.isalpha() or current_char == '~':
                    break

        # Handles SS3 sequences (F1–F4) starting with 'O' (ESC O P/Q/R/S) by skipping the following character (1 byte after 'ESC O' given that the 'O' has already been consumed previously)
        elif next_char == 'O':
            sys.stdin.read(1)

        else:
            pass  # Other escape sequences or unexpected bytes are ignored

    def handle_backspace() -> None:
        """Handles backspace: removes the last character from the password list and erases it from the console based on the selected mode."""
        if password:
            handle_char_timeout()
            password.pop()

            if mode in ('standard', 'last-char-temporary'):
                sys.stdout.write('\b \b' * mask_repeat)
                sys.stdout.flush()

            elif mode in ('pixel-lock', 'invisible'):
                pass  # No action needed for these modes on backspace

    def echo(char: str) -> None:
        """Appends a printable character to the password and displays the mask character based on the selected mode."""
        handle_char_timeout()
        password.append(char)

        if mode == 'standard':
            sys.stdout.write(mask * mask_repeat)

        elif mode == 'last-char-temporary':  # No support for multi-byte characters (e.g. emojis) and is partially compatible with mask_repeat
            sys.stdout.write(char * mask_repeat)
            sys.stdout.flush()
            time.sleep(last_char_visible_duration)
            sys.stdout.write('\b' * mask_repeat)
            sys.stdout.write(mask * mask_repeat)

        elif mode == 'pixel-lock':  # Same as previously noted
            sys.stdout.write(mask * mask_repeat)
            sys.stdout.write('\b' * mask_repeat)

        elif mode == 'invisible' or not mask:
            pass

        sys.stdout.flush()

    if os.name == 'nt':
        import msvcrt  # Windows-specific implementation using msvcrt

        while True:
            char = msvcrt.getwch()  # Reads the next character from msvcrt

            if handle_timeout():
                break
            if char in ('\r', '\n'):  # Enter key pressed
                break
            elif char == '\x03':  # Ctrl+C intercepted
                raise KeyboardInterrupt
            elif char in ('\x00', '\xe0') and msvcrt.getwch() != 'à':  # Skips special keys (e.g., arrows, function keys)
                # On Windows, msvcrt.getwch() returns '\x00' or '\xe0' as a prefix when a special key is pressed and a second call to getwch() retrieves the actual sequence
                # Notes: Some accented characters (like 'à') may require special handling on AZERTY keyboards. Ctrl+M/J (CR & LF) and Ctrl+H (BS) send the same sequences as Enter and Backspace (on Windows and POSIX systems)
                continue
            elif char == '\x08':  # Backspace (Windows)
                handle_backspace()
            elif char.isprintable():
                # Printable characters (letters, digits, symbols, etc.), adds to password and displays mask
                if char_limit is None or len(password) < char_limit:  # Enforces max character limit if set
                    echo(char)

    else:
        import termios, tty  # POSIX (Linux, macOS) specific implementation

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)  # Switches terminal to raw mode (no line buffering)

            while True:
                char = sys.stdin.read(1)  # Reads the next byte/character from stdin

                if handle_timeout():
                    break
                if char in ('\r', '\n'):  # Enter key
                    break
                elif char == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                elif char == '\x1b':  # Escape sequence (e.g., arrow keys)
                    skip_escape_sequence()
                    continue
                elif char == '\x7f':  # Backspace (POSIX)
                    handle_backspace()
                elif char.isprintable():  # Printable characters
                    if char_limit is None or len(password) < char_limit:  # Character limit
                        echo(char)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restoring terminal settings

    sys.stdout.write('\n')
    return ''.join(password)


# Usage:
if __name__ == '__main__':
    password = masked_input(
        prompt='Enter your password: ',
        mask='*',
        mask_repeat=2,
        timeout=10,
        timeout_prompt='Input timed out!',
        char_limit=20,
        mode='last-char-temporary'
    )

    print(f'Your password is: {password}')
