import os
import re
import solcx
from solcx.exceptions import SolcInstallationError

from mystery.solidity.solc_install import install_solc_version_select

PATTERN = re.compile(r"pragma solidity\s*(?:\^|>=|<=)?\s*(\d+\.\d+\.\d+)")


def check_string(re_exp, my_str):
    res = re.search(re_exp, my_str)
    if res:
        return True
    else:
        return False


def install_solcv(solc_ver):
    if check_string(r'(\d+\.\d+\.\d+)', solc_ver):
        try:
            solcx.install_solc(solc_ver)
            print("Solc v" + solc_ver + " installing")
            print("Solc v" + solc_ver + " installed.")
        except SolcInstallationError:
            print(f"v{solc_ver} is not available.")
    elif os.path.isfile(solc_ver):
        plist = os.path.splitext(solc_ver)
        if plist[1] in ['.sol']:
            with open(solc_ver, encoding="utf8") as file_desc:
                buf = file_desc.read()
                solc_ver_file = str(PATTERN.findall(buf))[2:-2]
                # print(len(solc_ver_file))
                if len(solc_ver_file) != 0:
                    try:
                        solcx.install_solc(solc_ver_file)
                        print("Solc v" + solc_ver_file + " installing")
                        print("Solc v" + solc_ver_file + " installed.")
                    except SolcInstallationError:
                        print(f"v{solc_ver} is not available.")
                else:
                    print("Sol version not found in this file.")
        else:
            print("Invalid *.sol File.")
    else:
        print("Input Error.")
