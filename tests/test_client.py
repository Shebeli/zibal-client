from zibal.client import ZibalIPGClient
from zibal.response_codes import WAGE_CODES, STATUS_CODES

REQUIRE_TRANSACTION_RESPONSE = {
    "message": "success",
    "result": 100,
    "trackId": 3714061657,
}

VERIFY_TRANSACTION_RESPONSE = {
    "message": "success",
    "result": 100,
    "refNumber": None,
    "paidAt": "2024-08-16T21:47:16.541000",
    "status": 1,
    "amount": 25000,
    "orderId": "",
    "description": "",
    "cardNumber": None,
    "multiplexingInfos": [],
}

INQUIRY_TRANSACTION_RESPONSE = {
    "message": "success",
    "result": 100,
    "refNumber": None,
    "paidAt": "2024-08-16T21:47:16.541000",
    "verifiedAt": "2024-08-16T21:47:50.629000",
    "status": 1,
    "amount": 25000,
    "orderId": "",
    "description": "",
    "cardNumber": None,
    "multiplexingInfos": [],
    "wage": 0,
    "shaparakFee": 1200,
    "createdAt": "2024-08-16T21:45:02.686000",
}  # a verified transaction


def test_transaction_require(mocker):
    # prepare the mock
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = REQUIRE_TRANSACTION_RESPONSE
    mock_response.status_code = 200
    mocker.patch("requests.post", return_value=mock_response)

    # prepare the client
    request_data = {
        "merchant": "zibal",
        "amount": 25000,
        "callback_url": "https://localhost:8000/",
    }
    client = ZibalIPGClient("zibal")
    response_data_model = client.request_transaction(**request_data)

    assert response_data_model.track_id == REQUIRE_TRANSACTION_RESPONSE["trackId"]
    assert response_data_model.result == REQUIRE_TRANSACTION_RESPONSE["result"]
    assert response_data_model.message == REQUIRE_TRANSACTION_RESPONSE["message"]


def test_transaction_verify(mocker):
    # prepare the mock
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = VERIFY_TRANSACTION_RESPONSE
    mock_response.status_code = 200
    mocker.patch("requests.post", return_value=mock_response)

    # for the sake of testing, we assume that the client has already requested
    # a transaction through request_transaction, and thus a track_id has
    # already been associated with the client.
    client = ZibalIPGClient("zibal")
    response_data_model = client.verify_transaction(track_id=3714061657)

    assert response_data_model.paid_at == VERIFY_TRANSACTION_RESPONSE["paidAt"]
    assert response_data_model.status == VERIFY_TRANSACTION_RESPONSE["status"]
    assert response_data_model.amount == VERIFY_TRANSACTION_RESPONSE["amount"]
    assert response_data_model.result == VERIFY_TRANSACTION_RESPONSE["result"]
    assert response_data_model.message == VERIFY_TRANSACTION_RESPONSE["message"]


def test_transaction_inquiry(mocker):
    # prepare the mock
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = INQUIRY_TRANSACTION_RESPONSE
    mock_response.status_code = 200
    mocker.patch("requests.post", return_value=mock_response)

    # client, assuming a transaction has already been verified
    client = ZibalIPGClient("zibal")
    response_data_model = client.inquiry_transaction(track_id=3714061657)

    assert response_data_model.status == INQUIRY_TRANSACTION_RESPONSE["status"]
    assert response_data_model.amount == INQUIRY_TRANSACTION_RESPONSE["amount"]
    assert (
        response_data_model.wage_meaning
        == WAGE_CODES[INQUIRY_TRANSACTION_RESPONSE["wage"]]
    )
    assert (
        response_data_model.status_meaning
        == STATUS_CODES[INQUIRY_TRANSACTION_RESPONSE["status"]]
    )
    assert response_data_model.message == INQUIRY_TRANSACTION_RESPONSE["message"]
