import pytest
from pydantic import ValidationError

from zibal.client import ZibalIPGClient
from zibal.response_codes import WAGE_CODES, STATUS_CODES
from tests.responses import (
    VALID_REQUIRE_RESPONSE,
    VALID_VERIFY_RESPONSE,
    VALID_INQUIRY_RESPONSE,
)


@pytest.fixture
def mock_request(mocker):
    def mock(return_data):
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = return_data
        mock_response.status_code = 200
        mocker.patch("requests.post", return_value=mock_response)

    return mock


def test_transaction_require(mock_request):
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
def test_invalid_transaction_require(request_data):
    client = ZibalIPGClient("zibal")
    with pytest.raises(ValidationError):
        client.request_transaction(**request_data)


def test_transaction_verify(mock_request):
    mock_request(VALID_VERIFY_RESPONSE)

    client = ZibalIPGClient("zibal")
    response_data_model = client.verify_transaction(track_id=3714061657)

    assert response_data_model.paid_at == VALID_VERIFY_RESPONSE["paidAt"]
    assert response_data_model.status == VALID_VERIFY_RESPONSE["status"]
    assert response_data_model.amount == VALID_VERIFY_RESPONSE["amount"]
    assert response_data_model.result == VALID_VERIFY_RESPONSE["result"]
    assert response_data_model.message == VALID_VERIFY_RESPONSE["message"]


def test_invalid_transaction_verify(mock_request):
    mock_request(VALID_VERIFY_RESPONSE)

    client = ZibalIPGClient("zibal")

    client.verify_transaction(track_id=3714061657)


def test_transaction_inquiry(mock_request):
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
