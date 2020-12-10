import os
import time

import blindspin
import crayons


def inside_container():
    return os.path.exists('/.dockerenv')


def wait_is_ready(func, max_tries=1000, sleep_timeout: float = 0.1):
    exception = None
    print(crayons.yellow("Waiting to be ready..."))
    with blindspin.spinner():
        for _ in range(0, max_tries):
            try:
                return func()
            except Exception as e:
                time.sleep(sleep_timeout)
                exception = e
        raise TimeoutError(
            'Wait time exceeded {0} sec. Method {1}, Exception {2}'.format(
                max_tries, func.__name__, exception))
