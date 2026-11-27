from typing import cast

from stock_collector.api.base_client import BaseAPIClient, DailyMarketData


class TWSEClient(BaseAPIClient):
    BASE_URL = "https://openapi.twse.com.tw/v1"

    DAILY_MARKET_ENDPOINT = "/exchangeReport/STOCK_DAY_ALL"

    def __init__(self) -> None:
        super().__init__(base_url=self.BASE_URL)

    def get_daily_market_data(self) -> list[DailyMarketData]:
        return cast(list[DailyMarketData], self.get(self.DAILY_MARKET_ENDPOINT))
