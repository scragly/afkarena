import typing as t

__all__ = (
    "RequestError", "UIDTypeError", "AuthTypeError", "AuthExpired", "AuthFailed",
    "CodeError", "CodeUsed", "CodeExpired", "CodeInvalid"
)


class RequestErrorBase(Exception):
    """Base logic for handling errors from returned AFK Arena requests."""
    __error_types__ = dict()
    _http_str: t.Optional[str]

    def __init_subclass__(cls, **kwargs):
        if hasattr(cls, "_http_str"):
            cls.__error_types__[cls._http_str] = cls

    @classmethod
    def get_error(cls, http_str: str):
        return cls.__error_types__.get(http_str, RequestError)


class RequestError(RequestErrorBase):
    """Exception raised when the AFK Arena API encountered an error."""
    _http_str = None


class UIDTypeError(RequestError):
    """Exception raised when the UID was not passed as a number."""
    _http_str = "err_uid_must_be_number"


class AuthTypeError(RequestError):
    """Exception raised when the auth code was not passed as a string."""
    _http_str = "err_code_must_be_valid_string"


class AuthExpired(RequestError):
    """Exception raised when Player is no longer authenticated."""
    _http_str = "err_login_state_out_of_date"


class AuthFailed(RequestError):
    """Exception raised when the incorrect authentication code was given."""
    _http_str = "err_wrong_code"


class CodeError(RequestError):
    """Exception raised when a gift code was unable to be redeemed."""
    pass


class CodeUsed(CodeError):
    """Exception raised when a gift code has already been used."""
    _http_str = "err_cdkey_batch_error"


class CodeExpired(CodeError):
    """Exception raised when a gift code has expired and can no longer be used."""
    _http_str = "err_cdkey_expired"


class CodeInvalid(CodeError):
    """Exception when an incorrect gift code was provided."""
    _http_str = "err_cdkey_record_not_found"
