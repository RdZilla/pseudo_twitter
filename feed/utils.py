from rest_framework import status
from rest_framework.response import Response


def validate_params(dict_for_validate, model_name):
    for param_name, param_value in dict_for_validate.items():
        if not param_value:
            response = {"errors": f"The {param_name} of {model_name} is missing."}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error
    return None
