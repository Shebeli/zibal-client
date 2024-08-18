class ResponseError(Exception):
    """Used for undesired HTTP response status codes."""

    pass


class TranscationError(Exception):
    """Used for errors related to transaction"""

    pass


class ResultError(Exception):
    """Used for result codes which are not successsfull (i.e. result code is not 100)"""

    pass
