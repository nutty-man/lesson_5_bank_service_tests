import logging
from typing import List, Any

import pytest


@pytest.fixture
def created_obj():
    objects: List[Any] = []
    yield objects
