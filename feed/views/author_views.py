from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, status, permissions

from feed.models import Author
from feed.serializers import AuthorsSerializer
from feed.statuses import SCHEMA_GET_POST_STATUSES, SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES, STATUS_204


class GetPostAuthorsView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['Authors'],
        summary="Get list of authors",
        responses={
            status.HTTP_200_OK: AuthorsSerializer,
            **SCHEMA_GET_POST_STATUSES
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Authors'],
        summary="Create new author",
        examples=[
            OpenApiExample(
                name='Example of an author create request',
                value={
                    "full_name": "Erich Maria Remarque",
                },
                request_only=True
            ),
        ],
        responses={
            status.HTTP_201_CREATED: AuthorsSerializer,
            **SCHEMA_GET_POST_STATUSES
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RetrieveUpdateDestroyAuthorView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=['Authors'],
        summary="Get author by id",
        responses={
            status.HTTP_200_OK: AuthorsSerializer,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Authors'],
        summary="Update author by id",
        examples=[
            OpenApiExample(
                name='Example of an author update request',
                value={
                    "full_name": "Erich Maria Remarque",
                },
                request_only=True
            ),
        ],
        responses={
            status.HTTP_200_OK: AuthorsSerializer,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=['Authors'],
        summary="Partial update author by id",
        examples=[
            OpenApiExample(
                name='Example of an author partial update request',
                value={
                    "full_name": "Erich Maria Remarque",
                },
                request_only=True
            ),
        ],
        responses={
            status.HTTP_200_OK: AuthorsSerializer,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=['Authors'],
        summary="Delete author by id",
        responses={
            **STATUS_204,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
