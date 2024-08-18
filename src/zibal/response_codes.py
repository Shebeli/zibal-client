# Zibal's result codes for requests
RESULT_CODES = {
    100: "Transaction verified successfully",
    102: "Given merchant was not found",
    103: "Given merchant is deactivated",
    104: "Given merchant is invalid",
    105: "Given 'amount' should be larger than 1,000 Rials",
    106: "Given callbackUrl is invalid (should start with http or https)",
    113: "Given 'amount' is larger than the transaction limit",
    201: "Transaction has already been verified",
    202: "Transaction has either failed or it hasn't been paid yet",
    203: "Given 'trackId' is invalid",
}


# Zibal's status codes for transaction states used in responses.
STATUS_CODES = {
    -1: "Waiting for payment",
    -2: "Internal Error",
    1: "Paid and verified",
    2: "Paid and unverified",
    3: "Cancelled by user",
    4: "Card number is invalid",
    5: "Not enough currency",
    6: "Entered password is incorrect",
    7: "Number of requests cannot exceed the limit",
    8: "Number of payment transactions cannot exceed the limit",
    9: "Daily's total paid amount cannot exceed the limit",
    10: "Card issuer is invalid",
    11: "Switch error",
    12: "Cart is inaccessible",
}

# Zibals's service fee deductions used in inquiry responses.
WAGE_CODES = {
    0: "Deduction from transaction",
    1: "Deduction from wallet",
    2: "Customer's responsiblity",
}
