from typing import List
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    # Now add the HTTP status code to the response.
    if response is not None:
        errors = []
        for field, message in response.data.items():
            print(message)
            if isinstance(message, list):
                message = message[0]
                
            errors.append({"field": field, "message": message})

        response.data = {"errors": errors}

    return response
