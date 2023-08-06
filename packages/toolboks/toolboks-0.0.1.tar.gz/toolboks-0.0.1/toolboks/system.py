"""
toolboks - Lightweight library & utility tools

Copyright (C) 2022 Mikael Tranbom

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import platform
import sys
import types


def context() -> types.SimpleNamespace:
    """Information about the current runtime and system environment"""
    system_context = types.SimpleNamespace()

    system_context.hostname = platform.node()
    system_context.machine = platform.machine()
    system_context.os = sys.platform
    system_context.platform = platform.platform()
    system_context.python_binary = sys.executable
    system_context.python_binary_real = os.path.realpath(sys.executable)
    system_context.python_implementation = platform.python_implementation()
    system_context.python_version = platform.python_version()
    system_context.system = platform.system()

    try:
        system_context.shell = os.environ['SHELL']
    except KeyError:
        system_context.shell = None

    try:
        system_context.user = os.environ['USER']
    except KeyError:
        system_context.user = None

    system_context.user_home = os.path.expanduser('~')

    try:
        system_context.virtual_environment = os.environ['VIRTUAL_ENV']
    except KeyError:
        system_context.virtual_environment = None

    return system_context
