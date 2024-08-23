class RequestError(Exception):
    """Used for errors related to requests, such as unexpected status codes, timeouts and etc."""

    pass


class TranscationError(Exception):
    """Used for errors related to transaction"""

    pass


class ResultError(Exception):
    """Used for result codes which are not successfull (i.e. result code is not 100)"""

    pass
