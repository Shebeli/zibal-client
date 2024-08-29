import logging
from enum import Enum
from logging import Logger
from typing import Optional, Union

import requests
from requests.exceptions import RequestException

from zibal.configs import IPG_BASE_URL, PAYMENT_BASE_URL
from zibal.exceptions import RequestError, ResultError
from zibal.models.schemas import (
    FailedResultDetail,
    TransactionInquiryRequest,
    TransactionInquiryResponse,
    TransactionRequireRequest,
    TransactionRequireRequestType,
    TransactionRequireResponse,
    TransactionVerifyRequest,
    TransactionVerifyResponse,
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
    `merchant` to `zibal` when initializing the class.

    If `raise_on_invalid_result` flag is set to True , when calling transaction
    related methods and the `result` code in the body of response is not 100,
    a `ResultError` exception will be raised.

    A `logger` instance can be passed for logging network requests.
    """

    def __init__(
        self,
        merchant: str,
        callback_url: str,
        raise_on_invalid_result: bool = False,
        request_timeout: int = 7,
        logger: Optional[Logger] = None,
    ):
        if logger is None:
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.NullHandler())
        else:
            self.logger = logger
        self.merchant = merchant
        self.raise_on_invalid_result = raise_on_invalid_result
        self.request_timeout = request_timeout
        self.callback_url = callback_url

    def _process_request(self, endpoint: ZibalEndPoints, data: dict) -> dict:
        url = IPG_BASE_URL + endpoint
        try:
            response = requests.post(url=url, json=data, timeout=self.request_timeout)
        except RequestException as err:
            self.logger.error(f"A network request error has occured: {err}")
            raise RequestError(f"A network request error has occured: {err}")

        if response.status_code != 200:
            self.logger.error(
                f"Unexpected response status code: {response.status_code} content: {response.content}"
            )
            raise RequestError(
                f"Unexpected response status code: {response.status_code} content: {response.content}"
            )
        self.logger.info(
            f"A successful HTTP request has been made to: {url} with data: {data}"
        )
        return response.json()

    def _validate_response(self, response_data: dict) -> Optional[FailedResultDetail]:
        """
        Since Zibal's responses status code is 200 under all circumenstances,
        any result codes other than 100 means the request was non-successful.
        """
        result_code = response_data.get("result", -100)
        if result_code != 100:
            if self.raise_on_invalid_result:
                result_message = RESULT_CODES.get(result_code, "Unknown result code")
                raise ResultError(result_message)
            return FailedResultDetail(
                result_code=result_code, result_meaning=RESULT_CODES[result_code]
            )
        return None

    def check_service_status(self) -> bool:
        """Check to see if the service is up and running, will log errors if there are any."""
        try:
            response = requests.head(IPG_BASE_URL, timeout=self.request_timeout)
            if response.status_code != 200:
                self.logger.warning(
                    f"Unexpected response status code on service check: {response.status_code} content: {response.content}"
                )
                return False

        except RequestException as err:
            self.logger.warning(
                f"A network request error has occured on service check: {err}"
            )
            return False

        return True

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

    @staticmethod
    def create_payment_link(track_id: int) -> str:
        """Constructs the payment link using track_id"""
        return PAYMENT_BASE_URL + str(track_id)
