from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


def success_response(message, data=None, status=status.HTTP_200_OK):
    if data:
        response = {
            "status": "success",
            "message": message,
            "data" : data
        }
    else:
        response = {
            "status": "success",
            "message": message,
        }
    return Response(response, status=status)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    response = {
        "status": "Bad request",
        "message": message,
        "status_code": status_code
    }
    return Response(response, status=status_code)


def set_auth_cookie(response, data):
    cookie_max_age = settings.COOKIE_MAX_AGE
    access = data.get(settings.ACCESS_TOKEN_COOKIE)
    refresh = data.get(settings.REFRESH_TOKEN_COOKIE)
    response.set_cookie(settings.ACCESS_TOKEN_COOKIE, access, max_age=cookie_max_age, httponly=True)

    if refresh:
        response.set_cookie(
            settings.REFRESH_TOKEN_COOKIE,
            refresh,
            max_age=cookie_max_age,
            httponly=True,
        )

        response.set_cookie(
            settings.REFRESH_TOKEN_LOGOUT_COOKIE,
            refresh,
            max_age=cookie_max_age,
            httponly=True,
        )


def reset_auth_cookie(response):
    response.delete_cookie(settings.ACCESS_TOKEN_COOKIE)
    response.delete_cookie(settings.REFRESH_TOKEN_COOKIE)
