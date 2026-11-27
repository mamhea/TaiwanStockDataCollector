from unittest.mock import patch

import pytest
import requests

from stock_collector.api.twse_client import DailyMarketData, TWSEClient


def test_get_daily_market_data() -> None:
    expected_data = [
        {
            "Date": "1151118",
            "Code": "2330",
            "Name": "台積電",
            "TradeVolume": "1000000",
            "TradeValue": "1500000000",
            "OpeningPrice": "1490.00",
            "HighestPrice": "1510.00",
            "LowestPrice": "1485.00",
            "ClosingPrice": "1500.00",
            "Change": "10.00",
            "Transaction": "5000",
        }
    ]

    with (
        TWSEClient() as client,
        patch.object(
            client,
            "get",
            return_value=expected_data,
        ) as mock_get,
    ):
        result: list[DailyMarketData] = client.get_daily_market_data()

    assert result == expected_data

    mock_get.assert_called_once_with("/exchangeReport/STOCK_DAY_ALL")


def test_get_daily_market_data_empty() -> None:
    with (
        TWSEClient() as client,
        patch.object(
            client,
            "get",
            return_value=[],
        ) as mock_get,
    ):
        result = client.get_daily_market_data()

    assert result == []

    mock_get.assert_called_once_with("/exchangeReport/STOCK_DAY_ALL")


def test_get_daily_market_data_request_error() -> None:
    with (
        TWSEClient() as client,
        patch.object(
            client,
            "get",
            side_effect=requests.ConnectionError("Connection failed"),
        ),
        pytest.raises(requests.ConnectionError),
    ):
        client.get_daily_market_data()
