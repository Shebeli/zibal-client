import logging

import pytest
from pydantic import ValidationError

from zibal.client import ZibalEndPoints, ZibalIPGClient
from zibal.configs import IPG_BASE_URL
from zibal.exceptions import ResultError
from zibal.response_codes import RESULT_CODES, STATUS_CODES, WAGE_CODES

from .responses import (
    ALREADY_VERIFIED_VERIFY_RESPONSE,
    FAILED_VERIFY_RESPONSE,
    NON_EXISTENT_VERIFY_RESPONSE,
    VALID_INQUIRY_RESPONSE,
    VALID_REQUIRE_RESPONSE,
    VALID_VERIFY_RESPONSE,
)


@pytest.fixture
def mock_request(mocker):
    def mock(return_data):
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = return_data
        mock_response.status_code = 200
        mocker.patch("requests.post", return_value=mock_response)

    return mock


@pytest.fixture
def logger_and_mock_logging(mocker):
    logger = logging.getLogger("zibal.client")
    mock_logging = mocker.patch.object(logger, "info")
    return logger, mock_logging


# --------------------------
# Transaction require Tests
# --------------------------


def test_valid_transaction_require(mocker, mock_request):
    # Prepare the mock
    mock_request(VALID_REQUIRE_RESPONSE)
    logger = logging.getLogger("zibal.client")
    mock_logging = mocker.patch.object(logger, "info")

    # Prepare the client and call the method
    request_data = {
        "amount": 25000,
        "callback_url": "https://localhost:8000/",
    }
    client = ZibalIPGClient("zibal", logger=logger)
    response_data_model = client.request_transaction(**request_data)

    # Prepare the expected log data
    expected_log_url = IPG_BASE_URL + ZibalEndPoints.REQUEST
    expected_log_data = {
        "merchant": "zibal",
        "amount": 25000,
        "callbackUrl": "https://localhost:8000/",
    }
    log_data = (
        f"A successful HTTP request has been made to: {expected_log_url} "
        f"with data: {expected_log_data}"
    )

    # Logging assertion
    mock_logging.assert_called_once_with(log_data)

    # Response assertion
    assert response_data_model.track_id == VALID_REQUIRE_RESPONSE["trackId"]
    assert response_data_model.result == VALID_REQUIRE_RESPONSE["result"]
    assert response_data_model.message == VALID_REQUIRE_RESPONSE["message"]


@pytest.mark.parametrize(
    "amount, callback_url",
    [
        (6969696969696969, "https://localhost:8000/"),
        (100, "https://localhost:8000/"),
        (50000, "invalid_url"),
        (50000, None),
        (None, "https://localhost:8000/"),
    ],
)
def test_transaction_require_raises_validation_error(amount, callback_url):
    # As long as the request data is valid, since the response is mocked, it
    # doesn't matter what is the request data
    client = ZibalIPGClient("zibal")
    with pytest.raises(ValidationError):
        client.request_transaction(amount=amount, callback_url=callback_url)


# --------------------------
# Transaction Verification
# --------------------------


def test_valid_transaction_verify(mocker, mock_request):
    # Prepare the mock
    mock_request(VALID_VERIFY_RESPONSE)
    logger = logging.getLogger("zibal.client")
    mock_logging = mocker.patch.object(logger, "info")

    # Prepare the client and call the method
    track_id = 12345
    client = ZibalIPGClient("zibal", logger=logger)
    response_data_model = client.verify_transaction(track_id=track_id)

    # Prepare the expected log data
    expected_url = IPG_BASE_URL + ZibalEndPoints.VERIFY
    expected_log_data = {"merchant": "zibal", "trackId": track_id}
    log_data = (
        f"A successful HTTP request has been made to: {expected_url} "
        f"with data: {expected_log_data}"
    )
    mock_logging.assert_called_once_with(log_data)

    assert response_data_model.paid_at == VALID_VERIFY_RESPONSE["paidAt"]
    assert response_data_model.status == VALID_VERIFY_RESPONSE["status"]
    assert response_data_model.amount == VALID_VERIFY_RESPONSE["amount"]
    assert response_data_model.result == VALID_VERIFY_RESPONSE["result"]
    assert response_data_model.message == VALID_VERIFY_RESPONSE["message"]


@pytest.mark.parametrize(
    "track_id",
    [
        "231323",
        "",
        123.323,
    ],
)
def test_transaction_verify_raises_validation_error(track_id):
    client = ZibalIPGClient("zibal")
    with pytest.raises(ValidationError):
        client.verify_transaction(track_id=track_id)


@pytest.mark.parametrize(
    "response_data",
    [
        FAILED_VERIFY_RESPONSE,
        NON_EXISTENT_VERIFY_RESPONSE,
        ALREADY_VERIFIED_VERIFY_RESPONSE,
    ],
)
def test_transaction_verify_raises_results_error(mock_request, response_data):
    mock_request(response_data)

    client = ZibalIPGClient("zibal", raise_on_invalid_result=True)
    with pytest.raises(ResultError) as exc_info:
        client.verify_transaction(track_id=1312333)
    assert RESULT_CODES[response_data.get("result")] in str(exc_info.value)


@pytest.mark.parametrize(
    "response_data",
    [
        FAILED_VERIFY_RESPONSE,
        NON_EXISTENT_VERIFY_RESPONSE,
        ALREADY_VERIFIED_VERIFY_RESPONSE,
    ],
)
def test_transaction_verify_returns_results_error(
    mock_request, response_data
):
    mock_request(response_data)

    client = ZibalIPGClient("zibal", raise_on_invalid_result=False)
    response_data_model = client.verify_transaction(track_id=123456)
    assert response_data_model.result_code == response_data["result"]
    assert response_data_model.result_meaning == RESULT_CODES.get(
        response_data["result"]
    )


# --------------------------
# Transaction Inquiry
# --------------------------


def test_valid_transaction_inquiry(mocker, mock_request):
    # Prepare the mock
    mock_request(VALID_INQUIRY_RESPONSE)
    logger = logging.getLogger("zibal.client")
    mock_logging = mocker.patch.object(logger, "info")

    # Prepare the client and call the method
    track_id = 12345
    client = ZibalIPGClient("zibal")
    response_data_model = client.inquiry_transaction(track_id=track_id)

    # Prepare the expected log data and assert the log
    expected_log_url = IPG_BASE_URL + ZibalEndPoints.INQUIRY
    expected_log_data = {"merchant": "zibal", "trackId": track_id}
    log_data = (
        f"A successful HTTP request has been made to: {expected_log_url} "
        f"with data: {expected_log_data}"
    )
    mock_logging.assert_called_once_with(log_data)

    # Assert response data
    assert response_data_model.status == VALID_INQUIRY_RESPONSE["status"]
    assert response_data_model.amount == VALID_INQUIRY_RESPONSE["amount"]
    assert (
        response_data_model.wage_meaning
        == WAGE_CODES[VALID_INQUIRY_RESPONSE["wage"]]
    )
    assert (
        response_data_model.status_meaning
        == STATUS_CODES[VALID_INQUIRY_RESPONSE["status"]]
    )
    assert response_data_model.message == VALID_INQUIRY_RESPONSE["message"]
