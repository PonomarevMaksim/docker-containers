import os
from logging import getLogger
from time import sleep
from typing import Callable

logger = getLogger(__name__)


def inside_container():
    return os.path.exists('/.dockerenv')


def wait_is_ready(func: Callable[[], bool], max_tries: int = 1000, sleep_timeout: float = 0.1):
    logger.debug('Waiting to be ready...')
    for _ in range(0, max_tries):
        if func():
            break
        sleep(sleep_timeout)
    else:
        raise TimeoutError(f'Max tries exceeded: {max_tries}. Method {func.__name__}')
