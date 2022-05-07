"""
从.sol文件中获取solc版本，若匹配多个版本，则返回最新版本list;若没有匹配的版本，则返回None
"""
import os
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_sol_version(sol_file):
    """
    获取solc版本
    :param sol_file: .sol文件
    :return: solc版本
    """
    # 如果文件后缀不是.sol，则提示错误
    if not sol_file.endswith('.sol'):
        logger.error('File extension is not .sol')
    else:
        # 如果文件存在，则获取文件中的智能合约版本
        if os.path.exists(sol_file):
            solc_version = []
            with open(sol_file, 'r') as f:
                for line in f:
                    if line.startswith('pragma solidity'):
                        version = re.findall(r'\d+\.\d+\.\d+', line)
                        if version:
                            solc_version.append(version[0])
            if solc_version:
                return max(solc_version)  # 返回最新版本
            else:
                return None
        else:
            logger.error('File does not exist')
