import hashlib
import random
import string
from typing import Union


def rdm_str(n: int):
    seed = string.digits + string.ascii_letters
    return ''.join(random.choices(seed, k=n))


def md5(data: Union[str, bytes]):
    if isinstance(data, str):
        data = data.encode(encoding='utf-8')
    return hashlib.md5(data).hexdigest()

