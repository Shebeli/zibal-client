from enum import Enum

import requests
from requests.models import Response

from zibal.configs import IPG_BASE_URL, PAYMENT_BASE_URL
from zibal.exceptions import ResponseError, ResultError
from zibal.models.schemas import (
    TransactionInquiryRequest,
    TransactionInquiryResponse,
    TransactionRequireRequest,
    TransactionRequireRequestType,
    TransactionRequireResponse,
    TransactionVerifyRequest,
    TransactionVerifyResponse,
)
from zibal.response_codes import RESULT_CODES


class ZibalEndPoints(str, Enum):
    REQUEST = "request"
    VERIFY = "verify"
    INQUIRY = "inquiry"


class ZibalIPGClient:
    """
    For testing IPG API endpoints, sandbox mode can be enabled by setting
    'merchant' to 'zibal' when initializing the class.
    """

    def __init__(self, merchant: str) -> None:
        self._merchant = merchant

    @property
    def merchant(self):
        return self._merchant

    def _handle_request(self, endpoint: ZibalEndPoints, data: dict) -> dict:
        url = self._construct_url(endpoint)
        response = requests.post(url=url, json=data)
        return self._handle_response(response)

    def _construct_url(self, endpoint: ZibalEndPoints) -> str:
        return IPG_BASE_URL + endpoint

    def _handle_response(self, response: Response) -> dict:
        """
        Since Zibal's responses status code is 200 under all circumenstances,
        the state of response is defined by the 'result' key in the response body.
        """
        if response.status_code != 200:
            raise ResponseError(
                f"An unexpected request error has occured \n status code: {response.status_code}, body: {response.content}"
            )
        response_data = response.json()
        result_code = response_data.get("result")
        if result_code != 100:
            error_msg = RESULT_CODES.get(result_code, f"Unknown result: {result_code}")
            raise ResultError(error_msg)
        return response_data

    def request_transaction(
        self, **kwargs: TransactionRequireRequestType
    ) -> TransactionRequireResponse:
        """
        Send a request to Zibal's IPG to initiate a new payment transaction.
        """
        request_model = TransactionRequireRequest(merchant=self.merchant, **kwargs)
        request_data = request_model.model_dump_to_camel(exclude_none=True)
        response_data = self._handle_request(ZibalEndPoints.REQUEST, request_data)
        return TransactionRequireResponse.from_camel_case(response_data)

    def create_payment_link(self, track_id: int) -> str:
        """Construct the payment link using track_id"""
        return PAYMENT_BASE_URL + str(track_id)

    def verify_transaction(self, track_id: int) -> TransactionVerifyResponse:
        """
        Sends a HTTP request for verifying an already started transaction,
        which will mark the end of the transaction.
        """
        request_model = TransactionVerifyRequest(
            merchant=self.merchant, track_id=track_id
        )
        request_data = request_model.model_dump_to_camel(exclude_none=True)
        response_data = self._handle_request(ZibalEndPoints.VERIFY, data=request_data)
        return TransactionVerifyResponse.from_camel_case(response_data)

    def inquiry_transaction(self, track_id: int) -> TransactionInquiryResponse:
        """
        Sends a HTTP request to retrieve the given transaction info
        """
        inquiry_model = TransactionInquiryRequest(
            merchant=self.merchant, track_id=track_id
        )
        request_data = inquiry_model.model_dump_to_camel(exclude_none=True)
        response_data = self._handle_request(ZibalEndPoints.INQUIRY, request_data)
        return TransactionInquiryResponse.from_camel_case(response_data)
