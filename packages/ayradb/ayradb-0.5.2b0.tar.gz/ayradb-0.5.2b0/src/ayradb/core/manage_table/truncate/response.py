__all__ = ['TruncateTableResponse', 'TruncateTableError']

from ayradb.rest.http.response import Response
from ayradb.core.parse import parse_error
from dataclasses import dataclass


class TruncateTableError:
    # Request errors (local)
    # AyraDB errors
    TABLE_NOT_FOUND = 1
    INTERNAL_ERROR = 100


ERROR_DICT = {
    "00005": TruncateTableError.TABLE_NOT_FOUND,
    # Errors that shouldn't happen since they are internally managed
    "00016": TruncateTableError.INTERNAL_ERROR,
}


@dataclass
class TruncateTableResponse:

    success: bool
    error_code: int
    _error_msg: str

    def __init__(self, success, error_code, _error_msg=""):
        self.success=success
        self.error_code=error_code
        self._error_msg=_error_msg

    @staticmethod
    def from_http_response(res: Response):
        if res.status_code == 200:
            return TruncateTableResponse(True, 0)
        else:
            # Case error returned by ayra
            error_msg = res.body.decode('ascii')
            try:
                error_code = ERROR_DICT[parse_error(error_msg)]
            except KeyError:
                error_code = TruncateTableError.INTERNAL_ERROR

            return TruncateTableResponse(False, error_code)


