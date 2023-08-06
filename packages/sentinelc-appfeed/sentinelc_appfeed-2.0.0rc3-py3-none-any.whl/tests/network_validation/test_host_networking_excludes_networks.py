import os

import pytest

from sentinelc_appfeed.builder import build_feed
from sentinelc_appfeed.utils.exceptions import ValidationError


BASEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/data"


def test_host_networking_excludes_networks():
    """
    A recipe kube cannot ask for hostNetwork: true in its spec file AND ask
    for networks configs at the same time.
    """
    with pytest.raises(ValidationError) as excinfo:
        build_feed(f"{BASEPATH}/host_networking")

    assert "hostNetwork" in str(excinfo.value)
