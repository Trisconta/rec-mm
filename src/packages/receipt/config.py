# config  (c)2025  Henrique Moreira

""" config -- a reader of $HOME/.receipts.cfg
"""

# pylint: disable=missing-function-docstring

import os
from os import environ

CONF_BASE = ".receipts.cfg"

DEF_DATA = {
    "RCPT": [],
}

class Config():
    """ config -- basic reader. """
    def __init__(self, bdir:str=""):
        c_home = bdir if bdir else ConfigHome()
        a_dir = bdir if bdir else c_home.home
        fname = os.path.join(a_dir, CONF_BASE)
        self._fname = fname
        self._has_file, self._data = self._read_config(fname)

    def config_file(self) -> str:
        """ Returns the path of the configuration file. """
        return self._fname

    def reload(self):
        self._has_file, self._data = self._read_config(self._fname)
        return self._has_file

    def config(self):
        return self._data["config"]

    def get_vars(self):
        return self._data["config"]

    def get_str(self, name, alt=None):
        item = self._data["config"].get(name)
        if item is None:
            return alt
        return item[0]

    def get_var(self, name):
        if not name:
            return []
        return self._data["config"][name]

    def main_path(self):
        paths = self.get_var("RCPT")
        return paths[0] if paths else "/"

    def _read_config(self, fname):
        if not fname:
            return {}
        text, dct = self._from_file(fname)
        a_data = {
            "text": text,
            "config": dct,
        }
        return True, a_data

    def _from_file(self, fname):
        dct = DEF_DATA
        try:
            with open(fname, "r", encoding="ascii") as fdin:
                text = fdin.read().rstrip("\n") + "\n"
        except FileNotFoundError:
            return "", dct
        for line in text.splitlines():
            what = line.strip()
            spl = what.split("=", maxsplit=1)
            if len(spl) == 1:
                dct[spl[0].strip()] = []
            else:
                lvalue, rvalue = spl[0].strip(), [spl[1].strip()]
                dct[lvalue] = rvalue
        return text, dct

    def stringify(self):
        astr = self._data["text"]
        return astr

    def __str__(self):
        return self.stringify()

    def __repr__(self):
        return repr(self.stringify())


class ConfigHome():
    """ Best-effort home path getter """
    def __init__(self):
        self.home = self.get_home()

    def get_home(self):
        home = environ.get("HOME")
        other = environ.get("USERPROFILE")
        if home is not None:
            return home
        if other is not None:
            return other
        if os.name == "linux":
            return "/"
        other = environ.get("SystemDrive")
        if other is None:
            return "C:/"
        return other

    def __str__(self):
        return self.home


#test = Config(); print(test, end="<<<\n"); print(test.get_vars())
