from functools import wraps
from typing import Callable


def map_output(mapper: Callable) -> Callable:
    def deco(function: Callable):
        @wraps(function)
        def impl(*args, **kwargs):
            return mapper(function(*args, **kwargs))

        return impl

    return deco
