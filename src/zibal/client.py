from enum import Enum
from typing import Union

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
    FailedResultDetail,
)
from zibal.response_codes import (
    RESULT_CODES,
)


class ZibalEndPoints(str, Enum):
    REQUEST = "request"
    VERIFY = "verify"
    INQUIRY = "inquiry"


class ZibalIPGClient:
    """
    For testing IPG API endpoints, sandbox mode can be enabled by setting
    'merchant' to 'zibal' when initializing the class.

    If `raise_result_error` flag is set to True , a `ResultError` exception
    will be raised if `result` code is not 100 in the body of responses.
    """

    def __init__(
        self,
        merchant: str,
        raise_result_error: bool = False,
    ) -> None:
        self._merchant = merchant
        self.raise_result_error = raise_result_error

    @property
    def merchant(self):
        return self._merchant

    def _process_request(self, endpoint: ZibalEndPoints, data: dict) -> dict:
        url = self._construct_url(endpoint)
        response = requests.post(url=url, json=data)
        return self._process_response(response)

    def _construct_url(self, endpoint: ZibalEndPoints) -> str:
        return IPG_BASE_URL + endpoint

    def _process_response(self, response: Response) -> dict:
        if response.status_code != 200:
            raise ResponseError(
                f"An unexpected request error has occured \n status code: {response.status_code}, body: {response.content}"
            )
        return response.json()

    def _validate_response(self, response_data: dict) -> FailedResultDetail | None:
        """
        Since Zibal's responses status code is 200 under all circumenstances,
        any result codes other than 100 means the request was non-successful.
        """
        result_code = response_data.get("result")
        if result_code != 100:
            if self.raise_result_error:
                result_message = RESULT_CODES.get(result_code, "Unknown result code")
                raise ResultError(result_message)
            return FailedResultDetail.from_camel_case(result_code=result_code)

    def request_transaction(
        self, **kwargs: TransactionRequireRequestType
    ) -> Union[TransactionRequireResponse, FailedResultDetail]:
        """
        Send a request to Zibal's IPG to initiate a new payment transaction.
        """
        request_model = TransactionRequireRequest(merchant=self.merchant, **kwargs)
        request_data = request_model.model_dump_to_camel(exclude_none=True, mode="json")
        response_data = self._process_request(ZibalEndPoints.REQUEST, request_data)
        result_error = self._validate_response(response_data)
        if result_error:
            return result_error
        return TransactionRequireResponse.from_camel_case(response_data)

    def create_payment_link(self, track_id: int) -> str:
        """Constructs the payment link using track_id"""
        return PAYMENT_BASE_URL + str(track_id)

    def verify_transaction(
        self, track_id: int
    ) -> Union[TransactionVerifyResponse, FailedResultDetail]:
        """
        Sends a HTTP request for verifying an already started transaction,
        which will mark the end of the transaction.
        """
        request_model = TransactionVerifyRequest(
            merchant=self.merchant, track_id=track_id
        )
        request_data = request_model.model_dump_to_camel(exclude_none=True)
        response_data = self._process_request(ZibalEndPoints.VERIFY, data=request_data)
        result_error = self._validate_response(response_data)
        if result_error:
            return result_error
        return TransactionVerifyResponse.from_camel_case(response_data)

    def inquiry_transaction(
        self, track_id: int
    ) -> Union[TransactionInquiryResponse, FailedResultDetail]:
        """
        Sends a HTTP request to retrieve the given transaction info.
        """
        inquiry_model = TransactionInquiryRequest(
            merchant=self.merchant, track_id=track_id
        )
        request_data = inquiry_model.model_dump_to_camel(exclude_none=True)
        response_data = self._process_request(ZibalEndPoints.INQUIRY, request_data)
        result_error = self._validate_response(response_data)
        if result_error:
            return result_error
        return TransactionInquiryResponse.from_camel_case(response_data)
