from drf_spectacular.utils import inline_serializer
from rest_framework import serializers, status

SCHEMA_PERMISSION_DENIED = {
    status.HTTP_401_UNAUTHORIZED: inline_serializer(
        "Unauthorized",
        {
            "detail": serializers.CharField(default="You do not have sufficient permissions to perform this action."),
        }
    ),
    status.HTTP_403_FORBIDDEN: inline_serializer(
        "Forbidden",
        {
            "detail_": serializers.CharField(default="Authentication credentials were not provided."),
        }
    )
}

STATUS_204 = {
    status.HTTP_204_NO_CONTENT: inline_serializer(
        "No Content",
        {
            "detail": serializers.CharField(default="No Content"),
        }
    )
}

STATUS_400 = {
    status.HTTP_400_BAD_REQUEST: inline_serializer(
        "Bad Request",
        {
            "detail": serializers.CharField(default="Bad Request"),
        }
    )
}

STATUS_404 = {
    status.HTTP_404_NOT_FOUND: inline_serializer(
        "Not Found",
        {
            "detail": serializers.CharField(default="Not Found"),
        }
    )
}

STATUS_500 = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: inline_serializer(
        "Internal Server Error",
        {
            "detail": serializers.CharField(default="Internal Server Error"),
        }
    )
}

GET_POST_SCHEMA_STATUSES = {
    **STATUS_400,
    **STATUS_500
}

RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES = {
    **STATUS_400,
    **STATUS_404,
    **STATUS_500
}
