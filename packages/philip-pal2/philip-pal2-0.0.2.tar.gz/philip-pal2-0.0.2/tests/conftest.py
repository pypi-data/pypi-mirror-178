"""
    Dummy conftest.py for philip_pal2.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import os

import pytest

# import pytest
from philip_pal2 import Phil

PHILIP_PAL2_LOCAL_PORT = os.getenv("PHILIP_PAL2_LOCAL_PORT")


@pytest.fixture(scope="module")
def phil_init_ex():
    print(PHILIP_PAL2_LOCAL_PORT)
    if PHILIP_PAL2_LOCAL_PORT:
        phil = Phil(port=PHILIP_PAL2_LOCAL_PORT)
    else:
        try:
            phil = Phil()
        except Exception as exc:
            pytest.skip(f"No real hardware preset: {exc}")
    yield phil


@pytest.fixture(scope="function")
def phil_ex(phil_init_ex: Phil):
    phil_init_ex.soft_reset()
    yield phil_init_ex
