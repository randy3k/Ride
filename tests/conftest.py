import pytest
import sys
import time
from .terminal import Terminal


def pytest_addoption(parser):
    parser.addoption(
        "--coverage", action="store_true", default=False, help="generate coverage report"
    )


@pytest.fixture(scope='session')
def radian_command(pytestconfig):
    if pytestconfig.getoption("coverage"):
        radian_command = [sys.executable, "-m", "radian", "--coverage"]
    else:
        radian_command = [sys.executable, "-m", "radian"]

    return radian_command


@pytest.fixture(scope='function')
def terminal(radian_command):
    with Terminal.open(radian_command) as t:
        yield t
        t.sendintr()
        t.write("q()\n")
        start_time = time.time()
        while t.isalive():
            if time.time() - start_time > 15:
                raise Exception("radian didn't quit cleanly")
            time.sleep(0.1)
