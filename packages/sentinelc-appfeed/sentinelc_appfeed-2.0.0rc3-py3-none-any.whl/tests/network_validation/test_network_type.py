import os

import pytest

from sentinelc_appfeed.builder import build_feed
from sentinelc_appfeed.utils.exceptions import ValidationError


BASEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/data"


def test_invalid_network_type():
    with pytest.raises(ValidationError) as excinfo:
        build_feed(f"{BASEPATH}/invalid_network_type")

    assert "type" in str(excinfo.value)
