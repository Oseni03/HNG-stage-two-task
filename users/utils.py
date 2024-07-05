from rest_framework.response import Response
from rest_framework import status


def success_response(message, data=None, status=status.HTTP_200_OK):
    response = {
        "status": "success",
        "message": message,
        "data" : data
    }
    return Response(response, status=status)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    response = {
        "status": "Bad request",
        "message": "Registration unsuccessful",
        "status_code": status_code
    }
    return Response(response, status=status_code)
