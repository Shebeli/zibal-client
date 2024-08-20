from zibal.models.schemas import (
    TransactionRequireRequest,
    TransactionRequireResponse,
    TransactionVerifyRequest,
    TransactionVerifyResponse,
)

from zibal.response_codes import STATUS_CODES


# Since the prefered string casing in python is snake case,
# while Zibal's IPG API endpoints handles the strings using camel case,
# The appropriate string transformation should take place depending on
# whether the process is serialization or deserialization.


def test_require_transaction_request_model():
    request_data = {
        "merchant": "zibal",
        "amount": 20000,
        "callback_url": "https://somecallbackurl.com",
    }  # data inputted by the client
    data_model = TransactionRequireRequest(**request_data)
    assert data_model.model_dump_to_camel(exclude_none=True, mode="json") == {
        "merchant": "zibal",
        "amount": 20000,
        "callbackUrl": "https://somecallbackurl.com/",
    }


def test_require_transaction_response_model():
    response_data = {
        "trackId": 1345,
        "result": 100,
        "message": "Some message",
    }  # data receieved from zibal IPG
    data_model = TransactionRequireResponse.from_camel_case(response_data)
    assert data_model.model_dump(exclude_none=True) == {
        "track_id": 1345,
        "result": 100,
        "message": "Some message",
    }


def test_verify_transaction_request_model():
    request_data = {
        "merchant": "zibal",
        "track_id": 12345,
    }  # data inputted by the client
    data_model = TransactionVerifyRequest(**request_data)
    assert data_model.model_dump_to_camel(exclude_none=True) == {
        "merchant": "zibal",
        "trackId": 12345,
    }


def test_verify_transaction_response_model():
    response_data = {
        "paidAt": "2024-02-26T20:47:34.429060",
        "cardNumber": "6037889125376713",
        "status": 1,
        "amount": 25000,
        "result": 100,
        "message": "some message",
        "orderId": "12",
        "multiplexingInfo": [],
    }  # data receieved from zibal IPG
    data_model = TransactionVerifyResponse.from_camel_case(response_data)
    assert data_model.model_dump(exclude_none=True) == {
        "paid_at": "2024-02-26T20:47:34.429060",
        "card_number": "6037889125376713",
        "status": 1,
        "status_meaning": STATUS_CODES.get(1),
        "amount": 25000,
        "result": 100,
        "message": "some message",
        "order_id": "12",
        "multiplexing_info": [],
    }
