import pandas as pd
import pytest

from tdxpy.constants import TDXParams
from tdxpy.exceptions import ValidationException
from tdxpy.logger import logger


def test_get_company_info_category(client):
    logger.info("查询公司信息目录")
    data = client.get_company_info_category(TDXParams.MARKET_SZ, "000001")
    assert data is not None
    assert type(data) is list
    assert len(data) > 0
    print(pd.DataFrame(data))


def test_get_company_info_category_raises(client):
    with pytest.raises(ValidationException):
        client.get_company_info_category()
