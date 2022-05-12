"""
安装智能合约solc版本
"""
import subprocess
import logging
import solcx
from solcx.exceptions import SolcInstallationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 使用solcx模块安装solc版本
def install_solc_version(solc_version):
    try:
        print("Solc v" + solc_version + " installing...")
        solcx.install_solc(solc_version)
        print("Solc v" + solc_version + " installed.")
    except SolcInstallationError as e:
        print("Solc v" + solc_version + " installing failed.")
        print(e)


# 使用solc-select模块安装并切换solc版本
def install_solc_version_select(solc_version):
    # print(solc_version)
    try:
        if solc_version is not None:
            subprocess.check_call(["solc-select", "use", solc_version])
        else:
            subprocess.check_call(["solc-select", "install", "0.8.13"])
            subprocess.check_call(["solc-select", "use", "0.8.13"])
    except Exception:
        print("Solc v" + solc_version + " installing...")
        subprocess.check_call(["solc-select", "install", solc_version])
        subprocess.check_call(["solc-select", "use", solc_version])
    except subprocess.CalledProcessError as e:
        print("Solc v" + solc_version + " installing failed.")
        print(e)
