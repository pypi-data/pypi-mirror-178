"""Decorators functions to be used in logging.

To be improved soon.
"""

import functools
from typing import Any, Callable, Optional

from loguru import logger


def logger_wraps(
    *,
    entry: Optional[bool] = True,
    exit: Optional[bool] = True,
    level: Optional[str] = "DEBUG"
) -> Callable:
    """Perform logging on function enter and exit.

    Args:
        entry (Optional[bool], optional): [description]. Defaults to True.
        exit (Optional[bool], optional): [description]. Defaults to True.
        level (Optional[str], optional): [description]. Defaults to "DEBUG".

    Returns:
        Callable: [description]
    """

    def wrapper(func: Callable) -> Callable:
        """Return wrapped function.

        Args:
            func (Callable): [description]

        Returns:
            Callable: [description]
        """
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> Any:
            """Decorate wrapped function.

            Returned type depends on function type and arguments.

            Returns:
                Any: [description]
            """
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper
