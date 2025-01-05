""" show_vars.py -- show configuration variables
(c)2025  Henrique Moreira
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "packages"))
from receipt.config import Config

def main():
    """ Main script. """
    cwd = os.getcwd()
    cfg = Config(cwd)
    dump_config(cfg)


def dump_config(cfg):
    """ dump configuration variables. """
    bdir = cfg.main_path()
    print("Config():", bdir)
    for key in sorted(cfg.get_vars()):
        item = repr(cfg.get_vars()[key])
        #astr = cfg.get_str(key)
        print(key, item, end="\n--\n")
    return True

# Main script
if __name__ == "__main__":
    main()
