import time
from typing import Self, TypedDict, TypeVar

import requests
from requests import Response, Session

from config.settings import REQUEST_RETRIES, REQUEST_TIMEOUT, RETRY_STATUS_CODES
from stock_collector.utils.logger import setup_logger

type JSONValue = (
    str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
)

type TimeoutType = int | float | tuple[float, float]

logger = setup_logger("stock_collector.api")

T = TypeVar("T")


class DailyMarketData(TypedDict):
    Date: str
    Code: str
    Name: str
    ClosingPrice: str


class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        timeout: TimeoutType = REQUEST_TIMEOUT,
        retries: int = REQUEST_RETRIES,
    ) -> None:

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries

        self.session: Session = requests.Session()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()

    def get(self, endpoint: str) -> JSONValue:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        for attempt in range(1, self.retries + 1):
            try:
                logger.info(
                    "Sending GET request: %s (attempt %d/%d)",
                    url,
                    attempt,
                    self.retries,
                )

                response: Response = self.session.get(
                    url,
                    timeout=self.timeout,
                )

                response.raise_for_status()

                try:
                    data = response.json()
                except requests.exceptions.JSONDecodeError:
                    logger.error(
                        "Invalid JSON response: %s",
                        url,
                    )
                    raise

                logger.info(
                    "Request successful: %s",
                    url,
                )

                return data

            except requests.exceptions.JSONDecodeError:
                raise

            except requests.RequestException as error:
                if isinstance(error, requests.HTTPError):
                    error_response = error.response

                    if error_response is None:
                        raise

                    status_code = error_response.status_code

                    if status_code not in RETRY_STATUS_CODES:
                        logger.error(
                            "Non-retryable HTTP error: %s (status: %d)",
                            url,
                            status_code,
                        )
                        raise

                logger.warning(
                    "Request failed: %s (%s)",
                    url,
                    error,
                )

                if attempt == self.retries:
                    logger.error(
                        "Maximum retry attempts reached: %s",
                        url,
                    )
                    raise

                delay = min(2 ** (attempt - 1), 30)

                logger.info(
                    "Retrying in %d seconds...",
                    delay,
                )

                time.sleep(delay)

        raise RuntimeError("Unexpected request failure")

    def close(self) -> None:
        self.session.close()
