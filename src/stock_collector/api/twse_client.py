from typing import TypeGuard

from stock_collector.api.base_client import BaseAPIClient, DailyMarketData, JSONValue


class TWSEClient(BaseAPIClient):
    BASE_URL = "https://openapi.twse.com.tw/v1"
    DAILY_MARKET_ENDPOINT = "/exchangeReport/STOCK_DAY_ALL"

    def __init__(self) -> None:
        super().__init__(base_url=self.BASE_URL)

    @staticmethod
    def _is_daily_market_data(
        item: JSONValue,
    ) -> TypeGuard[DailyMarketData]:
        if not isinstance(item, dict):
            return False

        required_string_fields = (
            "Date",
            "Code",
            "Name",
            "Change",
        )

        nullable_string_fields = (
            "TradeVolume",
            "TradeValue",
            "OpeningPrice",
            "HighestPrice",
            "LowestPrice",
            "ClosingPrice",
            "Transaction",
        )

        for field in required_string_fields:
            if not isinstance(item.get(field), str):
                return False

        for field in nullable_string_fields:
            value = item.get(field)

            if value is not None and not isinstance(value, str):
                return False

        return True

    def get_daily_market_data(self) -> list[DailyMarketData]:
        data = self.get(self.DAILY_MARKET_ENDPOINT)

        if not isinstance(data, list):
            raise TypeError("TWSE API response must be a list")

        records: list[DailyMarketData] = []

        for index, item in enumerate(data):
            if not self._is_daily_market_data(item):
                raise ValueError(f"Invalid TWSE market data at index {index}")

            records.append(item)

        return records
