"""
Get content of Solidity source code.
"""

import os
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# 读取sol文件，并返回json格式
def get_sol_content_json(sol_file):
    """
    Get content of Solidity source code.
    """
    # 如果文件后缀不是.sol，则提示错误
    if not sol_file.endswith('.sol'):
        logger.error('File extension is not .sol')
    else:
        # 如果文件存在，则获取文件内容
        if os.path.exists(sol_file):
            # print('File exists')
            # 读取solidity文件内容，并返回json格式
            with open(sol_file, 'r') as f:
                content = f.read()
                return json.dumps(content)
        else:
            logger.error('File does not exist')
