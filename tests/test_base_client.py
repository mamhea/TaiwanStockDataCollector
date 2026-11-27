from unittest.mock import Mock, patch

import pytest
import requests

from stock_collector.api.base_client import BaseAPIClient


@pytest.fixture
def client() -> BaseAPIClient:
    return BaseAPIClient(
        base_url="https://example.com/api",
        timeout=(5, 30),
        retries=3,
    )


def test_get_success(client: BaseAPIClient) -> None:
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}

    with patch.object(client.session, "get", return_value=mock_response) as mock_get:
        result = client.get("/stocks")

    assert result == {"status": "success"}

    mock_get.assert_called_once_with("https://example.com/api/stocks", timeout=(5, 30))


def test_get_http_error(client: BaseAPIClient) -> None:
    mock_response = Mock()

    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with (
        patch.object(client.session, "get", return_value=mock_response),
        patch("stock_collector.api.base_client.time.sleep"),
        pytest.raises(requests.HTTPError),
    ):
        client.get("/stocks")


def test_close(client: BaseAPIClient) -> None:
    with patch.object(client.session, "close") as mock_close:
        client.close()

    mock_close.assert_called_once()


def test_get_timeout(client: BaseAPIClient) -> None:
    with (
        patch.object(
            client.session, "get", side_effect=requests.Timeout("Connection timed out")
        ) as mock_get,
        patch("stock_collector.api.base_client.time.sleep"),
        pytest.raises(requests.Timeout),
    ):
        client.get("/stocks")

    assert mock_get.call_count == 3


def test_get_invalid_json(client: BaseAPIClient) -> None:
    mock_response = Mock()

    mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
        "Invalid JSON",
        "<html>",
        0,
    )

    with (
        patch.object(client.session, "get", return_value=mock_response) as mock_get,
        pytest.raises(requests.exceptions.JSONDecodeError),
    ):
        client.get("/stocks")

    mock_get.assert_called_once_with("https://example.com/api/stocks", timeout=(5, 30))


def test_get_non_retryable_http_error(client: BaseAPIClient) -> None:

    mock_response = Mock()
    mock_response.status_code = 404

    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "404 Not Found",
        response=mock_response,
    )

    with (
        patch.object(client.session, "get", return_value=mock_response) as mock_get,
        pytest.raises(requests.HTTPError),
    ):
        client.get("/stocks")

    mock_get.assert_called_once_with("https://example.com/api/stocks", timeout=(5, 30))


def test_get_retryable_http_error(client: BaseAPIClient) -> None:

    mock_response = Mock()
    mock_response.status_code = 503

    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "503 Service Unavailable",
        response=mock_response,
    )

    with (
        patch.object(
            client.session,
            "get",
            return_value=mock_response,
        ) as mock_get,
        patch("stock_collector.api.base_client.time.sleep"),
        pytest.raises(requests.HTTPError),
    ):
        client.get("/stocks")
    assert mock_get.call_count == 3


def test_context_manager_closes_session_on_exception(client: BaseAPIClient) -> None:

    with patch.object(client.session, "close") as mock_close:
        with pytest.raises(ValueError), client:
            raise ValueError("Test exception")

        mock_close.assert_called_once()


def test_get_retry_delay(client: BaseAPIClient) -> None:
    with (
        patch.object(
            client.session,
            "get",
            side_effect=requests.Timeout("Connection timed out"),
        ),
        patch("stock_collector.api.base_client.time.sleep") as mock_sleep,
        pytest.raises(requests.Timeout),
    ):
        client.get("/stocks")

    assert mock_sleep.call_count == 2
    assert mock_sleep.call_args_list == [
        ((1,),),
        ((2,),),
    ]


def test_get_retry_delay_maximum() -> None:
    client = BaseAPIClient(
        base_url="https://example.com/api",
        timeout=(5, 30),
        retries=7,
    )

    with (
        patch.object(
            client.session,
            "get",
            side_effect=requests.Timeout("Connection timed out"),
        ),
        patch("stock_collector.api.base_client.time.sleep") as mock_sleep,
        pytest.raises(requests.Timeout),
    ):
        client.get("/stocks")

    assert mock_sleep.call_args_list == [
        ((1,),),
        ((2,),),
        ((4,),),
        ((8,),),
        ((16,),),
        ((30,),),
    ]
