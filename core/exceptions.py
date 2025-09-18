from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({"errors": response.data}, status=response.status_code)

    return Response(
        {"errors": {"detail": str(exc)}}, status=status.HTTP_400_BAD_REQUEST
    )

