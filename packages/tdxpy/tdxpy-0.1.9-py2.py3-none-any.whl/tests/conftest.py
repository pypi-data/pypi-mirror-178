import json
from pathlib import Path

import pytest

from tdxpy.hq import TdxHq_API


@pytest.fixture
def bestip():
    config = Path(Path.home() / ".mootdx/config.json").read_text()
    config = json.loads(config)
    ip, port = config.get("BESTIP")["HQ"]

    print(bestip)

    return ip, int(port)


@pytest.fixture(scope="session")
def client():
    config = Path(Path.home() / ".mootdx/config.json").read_text()
    config = json.loads(config)
    bestip = config.get("BESTIP")["HQ"]

    api = TdxHq_API()
    api.connect(ip=bestip[0], port=int(bestip[1]))

    return api
