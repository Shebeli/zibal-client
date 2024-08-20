VALID_REQUIRE_RESPONSE = {
    "message": "success",
    "result": 100,
    "trackId": 3714061657,
}

# verify different responses:
VALID_VERIFY_RESPONSE = {
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
# failuire cases:
NON_EXISTENT_VERIFY_RESPONSE = {"message": "trackId not found", "result": 203}
FAILED_VERIFY_RESPONSE = {"message": "transaction failed", "result": 202}
ALREADY_VERIFIED_VERIFY_RESPONSE = {"message": "previously verifed", "result": 201}

# Inquiry different responses
VALID_INQUIRY_RESPONSE = {
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
