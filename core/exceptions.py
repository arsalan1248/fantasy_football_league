from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 401:
        return Response(
            {
                "error": "Authentication failed",
                "detail": "Token is invalid or expired",
                "status_code": 401,
            },
            status=401,
        )

    return response
