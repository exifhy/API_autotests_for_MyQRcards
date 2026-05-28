import time
from typing import Callable, Optional, TypeVar


T = TypeVar("T")


def wait_until(predicate: Callable[[], Optional[T]], timeout_s: int = 60, step_s: float = 3.0) -> Optional[T]:
    end = time.time() + timeout_s
    last = None
    while time.time() < end:
        last = predicate()
        if last is not None:
            return last
        time.sleep(step_s)
    return None
