import pytest
from pydantic import ValidationError

from zibal.response_codes import RESULT_CODES
from zibal.client import ZibalIPGClient
from zibal.response_codes import WAGE_CODES, STATUS_CODES
from .responses import (
    VALID_REQUIRE_RESPONSE,
    VALID_VERIFY_RESPONSE,
    VALID_INQUIRY_RESPONSE,
    FAILED_VERIFY_RESPONSE,
    NON_EXISTENT_VERIFY_RESPONSE,
    ALREADY_VERIFIED_VERIFY_RESPONSE,
)
from zibal.exceptions import ResultError


@pytest.fixture
def mock_request(mocker):
    def mock(return_data):
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = return_data
        mock_response.status_code = 200
        mocker.patch("requests.post", return_value=mock_response)

    return mock


# --------------------------
# Transaction require
# --------------------------


def test_valid_transaction_require(mock_request):
    mock_request(VALID_REQUIRE_RESPONSE)

    # prepare the client
    request_data = {
        "amount": 25000,
        "callback_url": "https://localhost:8000/",
    }
    client = ZibalIPGClient("zibal")
    response_data_model = client.request_transaction(**request_data)

    assert response_data_model.track_id == VALID_REQUIRE_RESPONSE["trackId"]
    assert response_data_model.result == VALID_REQUIRE_RESPONSE["result"]
    assert response_data_model.message == VALID_REQUIRE_RESPONSE["message"]


@pytest.mark.parametrize(
    "request_data",
    [
        ({"amount": 6969696969696969, "callback_url": "https://localhost:8000/"}),
        ({"amount": 100, "callback_url": "https://localhost:8000/"}),
        ({"amount": 50000, "callback_url": "invalid_url"}),
        ({"amount": 50000}),
        ({"callback_url": "https://localhost:8000/"}),
    ],
)
def test_transaction_require_raises_validation_error(request_data):
    # As long as the request data is valid, since the response is mocked, it
    # doesn't matter what is the request data
    client = ZibalIPGClient("zibal")
    with pytest.raises(ValidationError):
        client.request_transaction(**request_data)


# --------------------------
# Transaction Verification
# --------------------------


def test_valid_transaction_verify(mock_request):
    mock_request(VALID_VERIFY_RESPONSE)

    client = ZibalIPGClient("zibal")
    response_data_model = client.verify_transaction(track_id=3714061657)

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
def test_transaction_verify_returns_results_error(mock_request, response_data):
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


def test_valid_transaction_inquiry(mock_request):
    # prepare the mock
    mock_request(VALID_INQUIRY_RESPONSE)

    # client, assuming a transaction has already been verified
    client = ZibalIPGClient("zibal")
    response_data_model = client.inquiry_transaction(track_id=3714061657)

    assert response_data_model.status == VALID_INQUIRY_RESPONSE["status"]
    assert response_data_model.amount == VALID_INQUIRY_RESPONSE["amount"]
    assert (
        response_data_model.wage_meaning == WAGE_CODES[VALID_INQUIRY_RESPONSE["wage"]]
    )
    assert (
        response_data_model.status_meaning
        == STATUS_CODES[VALID_INQUIRY_RESPONSE["status"]]
    )
    assert response_data_model.message == VALID_INQUIRY_RESPONSE["message"]
