import json
from django.utils.translation import ugettext as _
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ErrorDetail
from . import settings
from .utils import is_pretty


def friendly_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if not response and settings.CATCH_ALL_EXCEPTIONS:
        exc = APIException(exc)
        response = exception_handler(exc, context)

    if response is not None:
        if is_pretty(response):
            return response
        error_message = ''
        for key, value in response.data.items():
            if not type(value[0]) is dict:
                error_message = _(str(value))
            if type(value[0]) is ErrorDetail:
                error_message = _(str(value[0]))
        error_code = settings.FRIENDLY_EXCEPTION_DICT.get(
            exc.__class__.__name__)
        response.data['message'] = error_message
        response.data['status_code'] = response.status_code
    return response
