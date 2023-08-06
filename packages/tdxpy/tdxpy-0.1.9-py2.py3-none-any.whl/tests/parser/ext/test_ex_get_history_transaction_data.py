import pytest


@pytest.mark.skip
def test_ex_get_history_transaction_data(client):
    assert client.to_df(client.get_history_transaction_data(47, "IFL0", 20170811))
