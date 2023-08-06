from pprint import pprint

import pytest

from tdxpy.constants import TDXParams
from tdxpy.exceptions import ValidationException
from tdxpy.logger import logger


def test_get_company_info_content(client):
    logger.info("查询公司信息目录")
    data = client.get_company_info_category(TDXParams.MARKET_SZ, "000001")

    assert data
    assert len(data) > 0

    logger.info('读取公司信息-最新提示')
    data = client.get_company_info_content(0, '000001', '000001.txt', data[0]['start'], data[0]['length'])

    assert data
    assert len(data) > 0
    pprint(data)


def test_get_company_info_content_raises(client):
    with pytest.raises(ValidationException):
        client.get_company_info_content()
