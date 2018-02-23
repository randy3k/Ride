from __future__ import unicode_literals
import os
import sys

from prompt_toolkit.eventloop.context import TaskLocal, TaskLocalNotSetError
from prompt_toolkit.filters import to_filter
from prompt_toolkit.utils import is_windows, is_conemu_ansi
from .base import Output

from six import PY2

__all__ = [
    'create_output',
    'get_default_output',
    'set_default_output',
]


def create_output(stdout=None, true_color=False, ansi_colors_only=None):
    """
    Return an :class:`~prompt_toolkit.output.Output` instance for the command
    line.

    :param true_color: When True, use 24bit colors instead of 256 colors.
        (`bool` or :class:`~prompt_toolkit.filters.Filter`.)
    :param ansi_colors_only: When True, restrict to 16 ANSI colors only.
        (`bool` or :class:`~prompt_toolkit.filters.Filter`.)
    """
    stdout = stdout or sys.__stdout__
    true_color = to_filter(true_color)

    if is_windows():
        from .conemu import ConEmuOutput
        from .win32 import Win32Output
        from .windows10 import is_win_vt100_enabled, Windows10_Output

        if is_win_vt100_enabled():
            return Windows10_Output(stdout)
        if is_conemu_ansi():
            return ConEmuOutput(stdout)
        else:
            return Win32Output(stdout)
    else:
        from .vt100 import Vt100_Output
        term = os.environ.get('TERM', '')
        if PY2:
            term = term.decode('utf-8')

        return Vt100_Output.from_pty(
            stdout, true_color=true_color,
            ansi_colors_only=ansi_colors_only, term=term)


_default_output = TaskLocal()


def get_default_output():
    """
    Get the output class to be used by default.

    Called when creating a new Application(), when no `Output` has been passed.
    """
    try:
        value = _default_output.get()
    except TaskLocalNotSetError:
        return create_output()
    else:
        return value


def set_default_output(output):
    """
    Set the default `Output` class.
    """
    assert isinstance(output, Output)
    _default_output.set(output)
