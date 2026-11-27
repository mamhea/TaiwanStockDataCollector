import pytest

from stock_collector.api.base_client import DailyMarketData
from stock_collector.api.twse_client import TWSEClient


@pytest.fixture(scope="module")
def market_data() -> list[DailyMarketData]:
    with TWSEClient() as client:
        return client.get_daily_market_data()


def test_response_is_list(market_data: list[DailyMarketData]) -> None:
    assert isinstance(market_data, list)


def test_response_is_not_empty(market_data: list[DailyMarketData]) -> None:
    assert len(market_data) > 0


def test_required_fields_exist(market_data: list[DailyMarketData]) -> None:
    required_fields = {
        "Date",
        "Code",
        "Name",
        "TradeVolume",
        "TradeValue",
        "OpeningPrice",
        "HighestPrice",
        "LowestPrice",
        "ClosingPrice",
        "Change",
        "Transaction",
    }

    for record in market_data:
        assert required_fields.issubset(record.keys())


def test_stock_codes_are_unique(market_data: list[DailyMarketData]) -> None:
    codes = [record["Code"] for record in market_data]

    assert len(codes) == len(set(codes))


@pytest.mark.parametrize("field", ["Date", "Code", "Name"])
def test_required_fields_are_not_empty(
    market_data: list[DailyMarketData],
    field: str,
) -> None:
    for record in market_data:
        assert record.get(field) not in (None, "")


@pytest.mark.parametrize(
    "field",
    [
        "TradeVolume",
        "TradeValue",
        "OpeningPrice",
        "HighestPrice",
        "LowestPrice",
        "ClosingPrice",
        "Change",
        "Transaction",
    ],
)
def test_numeric_fields_contain_valid_numbers(
    market_data: list[DailyMarketData],
    field: str,
) -> None:
    for record in market_data:
        value = record.get(field)

        if value in (None, ""):
            continue

        try:
            float(value)
        except ValueError, TypeError:
            pytest.fail(f"Invalid numeric value in {field}: {value!r}")
