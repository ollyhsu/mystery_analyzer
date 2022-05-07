import logging
from functools import lru_cache
import _pysha3

log = logging.getLogger(__name__)


# change the bytecode to bytes
@lru_cache(maxsize=2 ** 10)
def get_code_hash(code) -> str:
    if type(code) == tuple:
        return str(hash(code))
    code = code[2:] if code[:2] == "0x" else code
    # print(code)
    try:
        keccak = _pysha3.keccak_256()
        keccak.update(bytes.fromhex(code))
        return "0x" + keccak.hexdigest()
    except ValueError:
        log.debug("Unable to change the bytecode to bytes. Bytecode: {}".format(code))
        return ""


# print(get_code_hash("0x000000"))
