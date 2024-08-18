from typing import List, Literal, Optional, TypedDict, NotRequired

from pydantic import BaseModel, ConfigDict, field_validator
from zibal.utils import to_camel_case_dict, to_snake_case_dict

from zibal.response_codes import STATUS_CODES, WAGE_CODES


# All of the data models with the word 'Request' ending in their name are
# the data structures used in body of HTTP requests, while the data models
# ending  with 'Response' are the data structures that are expected to be
# received from the IPG APIs responses.

ResultCode = Literal[100, 102, 103, 104, 105, 106, 113]
FeeDeductionCodes = Literal[0, 1, 2]
StatusCode = Literal[-1, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
WageCode = Literal[0, 1, 2]
IsoDate = str  # e.g. '2024-08-11T16:06:44.731255'


class TransaactionBaseModel(BaseModel):
    def model_dump_to_camel(self, **kwargs) -> dict:
        """
        Same as model_dump method, but convert the snake case keys into camel
        case keys. Pass any passed kwargs to model_dump.
        """
        data = self.model_dump(**kwargs)
        return to_camel_case_dict(data)

    @classmethod
    def from_camel_case(cls, data: dict) -> "TransaactionBaseModel":
        """Initialize an instance by converting the dict camel case keys to snake case keys."""
        data = to_snake_case_dict(data)
        return cls(**data)


class TransactionRequireRequest(TransaactionBaseModel):
    """Used for starting a transaction process."""

    model_config = ConfigDict(strict=True)

    merchant: str
    amount: int
    callback_url: str
    description: Optional[str] = None
    order_id: Optional[str] = None
    mobile: Optional[str] = None
    allowed_cards: List[str] | None = None
    ledger_id: Optional[str] = None
    national_code: str = None

    @field_validator("amount")
    def minimum_amount(cls, amount):
        if amount < 1500:
            raise ValueError("Amount must be larger than 1500")
        return amount


# Serialization: model instance (python) -> JSON data (or any kind of primtive data)
# Deserialization:  JSON data (or data from client) -> model instance (python)
class TransactionRequireRequestType(TypedDict):
    """Used only for type annotating"""

    merchant: str
    amount: int
    callback_url: str
    description: NotRequired[str]
    order_id: NotRequired[str]
    mobile: NotRequired[str]
    allowed_cards: NotRequired[[List[str]]]
    ledger_id: NotRequired[str]
    national_code: NotRequired[str]


class TransactionRequireResponse(TransaactionBaseModel):
    track_id: int
    result: ResultCode
    pay_link: Optional[str] = None
    message: str

    

class TransactionCallbackQueryParams(TransaactionBaseModel):
    """
    A GET HTTP request is called from zibal's webservice to the provided callbackUrl
    (the callbackUrl should have been provided in earlier levels of
    transaction process).
    The request is called with query parameters following this class's data
    structure.
    """

    success: Literal[1, 0]  # 1 for success, 0 for failure
    track_id: int
    order_id: str
    status: StatusCode


class TransactionVerifyRequest(TransaactionBaseModel):
    """Transactions that need to be verified by the app"""

    model_config = ConfigDict(strict=True)

    merchant: str
    track_id: int


class TransactionVerifyResponse(TransaactionBaseModel):
    paid_at: IsoDate
    card_number: Optional[str] = None
    status: StatusCode
    status_meaning: str
    amount: int
    ref_number: Optional[int] = None  # if successful
    description: Optional[str] = None  # if successful
    order_id: Optional[str] = None  # if successful
    result: ResultCode
    message: str
    multiplexing_info: List[str] = []

    @classmethod
    def from_camel_case(cls, data: dict) -> TransaactionBaseModel:
        data["status_meaning"] = STATUS_CODES.get(data.get("status"), "Unknown status")
        return super().from_camel_case(data)

class TransactionInquiryRequest(TransaactionBaseModel):
    """For inquirying the state of an already started transaction"""

    model_config = ConfigDict(strict=True)

    merchant: str
    track_id: int


class TransactionInquiryResponse(TransaactionBaseModel):
    created_at: IsoDate
    paid_at: IsoDate
    verified_at: IsoDate
    card_number: Optional[str] = None
    status: StatusCode
    status_meaning: str
    amount: int
    ref_number: Optional[int] = None  # if successful
    description: str
    order_id: Optional[str] = None
    wage: WageCode
    wage_meaning: str
    shaparak_fee: int
    result: ResultCode
    message: str
    multiplexing_info: List[str] = []

    @classmethod
    def from_camel_case(cls, data: dict) -> TransaactionBaseModel:
        data["status_meaning"] = STATUS_CODES.get(data.get("status"), "Unknown status")
        data["wage_meaning"] = WAGE_CODES.get(data.get("wage"), "Unknown wage")
        return super().from_camel_case(data)
