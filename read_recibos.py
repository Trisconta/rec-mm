""" read_recibos.py
(c)2025  Henrique Moreira
"""

import sys
import os.path
#import openpyxl
#from openpyxl.utils import get_column_letter
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "packages"))
from receipt.config import Config

NOW_YEAR = 2025

MONTHS = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Marco",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

FIELDS_1 = {
    "E7": ("month", "Janeiro", "s"),
    "F7": ("year", 2023, "n"),
    "B9": ("floor", 1, "n"),
    "C9": ("letter", "A", "s"),
    "H9": ("perm", "Permilagem", "s"),
    "I9": ("permil", 0.195, "n"),
    "D14": ("t_value", "Valor do Condominio", "s"),
    "G14": ("condo_v1", 33.5, "n"),
    "D15": ("t_f_res", "Fundo de Reserva", "s"),
    "G15": ("condo_v2", 5.85, "s"),
    "D16": ("t_other", "", "s"),
    "G16": ("condo_v3", 0.0, "n"),
    # Fixed stuff
    "A1": ("designation", "Administracao", "s"),
    "A2": ("nif", "NIF: %s", "s"),
    "A3": ("iban", "PT050xxx", "s"),
    "A4": ("mail", "E-mail: ruamariamachado2@gmail.com", "s"),
}

EAST_2 = {
    "E7": "O7",
    "F7": "P7",
}

SOUTH_2 = {
    "E7": "E34",
    "F7": "F34",
}

def main():
    cfg = Config()
    bdir = cfg.main_path()
    assert bdir, cfg.config_file()
    fname = "../../snippets/xecibos/2023_Recibos_Condominio.xlsx"
    fname = "/opt/local/temp/rec2.xlsx"
    tups = (
        FIELDS_1,
        EAST_2,
        SOUTH_2,
    )
    hsh = build_hash(tups, cfg)
    print("Debug:")
    for key in hsh: print(key, hsh[key], end="\n\n")
    #read_wbk(fname, tups)


def coluna(num):
    assert num >= 1, num
    try:
        astr = get_column_letter(num)
    except NameError:
        astr = (chr(ord("A") + num - 1)) if 0 < num <= 26 else "zz"
    return astr

def read_wbk(fname, hsh):
    wbk = openpyxl.open(fname, data_only=True)
    dct = {
        "Workbook": wbk,
        "Sheets": [],
    }
    for s_name in wbk.sheetnames:
        page = wbk[s_name]
        dct["Sheets"].append(page)
    return wbk, dct

def build_hash(tups, cfg):
    hsh = {}
    fields, east, south = tups
    # January is FIELDS_1
    key = sorted(east)[0]
    diff = ord(east[key][0]) - ord(key[0])
    cnt = 1
    for mth in MONTHS:
        hsh[mth] = {}
        for key in fields:
            new = coluna(ord(key[0]) - ord("A") + cnt) + key[1:]
            tup = fields[key]
            fld, data, data_type = tup
            if fld == "month":
                data = MONTHS[mth]
            elif fld == "year":
                data = NOW_YEAR
            elif fld == "designation":
                data = cfg.get_str("DESIGN")
            elif fld == "nif":
                data = cfg.get_str("NIF")
            elif fld == "iban":
                data = cfg.get_str("IBAN")
            elif fld == "mail":
                what = cfg.get_str("MAIL")
                assert data == what, f"mth={ mth}, {repr(data)} vs {repr(what)}"
            item = [fld, data, data_type]
            if mth == 1:
                hsh[mth][key] = item
            else:
                hsh[mth][new] = item
                
        cnt += diff
    return hsh

main()
