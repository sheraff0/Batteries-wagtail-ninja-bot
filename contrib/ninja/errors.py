import json

from django.conf import settings

from ninja.errors import ValidationError, HttpError


def validation_error_handler(app):
    def _(request,
        exc: ValidationError
    ):
        _code = settings.AE.VALIDATION_ERROR
        _detail = settings.API_ERRORS_FLAT[_code]
        print(exc.errors)
        return app.create_response(
            request,
            {
                "code": _code,
                "detail": _detail,
                "errors": {
                    ".".join(map(str, error["loc"][2:])) or "non_field_errors": [error["msg"]]
                    for error in exc.errors
                },
            },
            status=422,
        )
    return _


def http_error_handler(app):
    def _(request,
        exc: HttpError
    ):
        _message = exc.message
        # Try parse message as json object with (optionally) `code`, `detail`
        try:
            _message = json.loads(_message)
            _code = _message.pop("code", None)
            _detail = _message.pop("detail", None)
        # Treated as string by default
        except:
            _code = _message
            _detail = None
            _message = {}

        # Try get `code` interpretation from settings.API_ERRORS dictionary.
        # Custom `detail` is prioritized
        _from_dict = settings.API_ERRORS_FLAT.get(_code)
        if _from_dict:
            _detail = _detail or _from_dict
        # If `code` cannot be interpreted, then it's passed as `detail`
        else:
            _detail, _code = _detail or _code, None
        _message["detail"] = _detail

        return app.create_response(
            request,
            {
                **({"code": _code} if _code is not None else {}),
                **_message,
            },
            status=exc.status_code,
        )
    return _
