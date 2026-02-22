from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data
    if isinstance(detail, dict) and 'detail' in detail:
        detail = detail['detail']

    response.data = {
        'error': {
            'code': response.status_code,
            'message': str(detail),
            'details': response.data,
        }
    }
    return response
