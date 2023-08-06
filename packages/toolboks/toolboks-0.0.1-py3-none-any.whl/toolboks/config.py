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
import configparser
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, Literal, overload


@overload
def read_config(file: str, as_dict: Literal[False] = False) -> SimpleNamespace:
    ...


@overload
def read_config(file: str, as_dict: Literal[True]) -> Dict:
    ...


@overload
def read_config(file: str, as_dict: bool) -> Dict | SimpleNamespace:
    ...


def read_config(file: str, as_dict: bool = False):
    """
    Read a configuration file and return as either a SimpleNamespace
    object or as a dict if `as_dict` is True
    """
    filepath = Path(file)

    if not filepath.is_file():
        raise FileNotFoundError("Invalid filename")

    config_file = configparser.ConfigParser()
    config_file.read(str(filepath))

    config = SimpleNamespace()

    for section in config_file.sections():
        section_nsp = SimpleNamespace()

        for key in config_file[section]:
            value = config_file[section][key]
            setattr(section_nsp, key, value)

        setattr(config, section, section_nsp)
        del section_nsp

    if as_dict:
        conf_dict = config.__dict__

        for key in conf_dict:
            if isinstance(conf_dict[key], SimpleNamespace):
                conf_dict[key] = conf_dict[key].__dict__

        return conf_dict
    return config
