import functools
from typing import Callable, TypeVar
from models import Case


__T = TypeVar("__T", bound=Case)


def case(test: Callable, info: __T | None) -> Callable:
    """
    Testable case decorator for PyTest tests.2

    Parameters
    ----------
    test : Callable
        PyTest test to initialize as a Testable case

    info : __T | None
        Case information to add to the Testable case

    Returns
    -------
    decorated_test : Callable
        Test decorated with Testable functionality
    """
    @functools.wraps(test)
    def wrapper(*args, **kwargs):
        test(*args, **kwargs)

    return wrapper
