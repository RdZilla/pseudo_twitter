from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, permissions

from feed.models import Author
from feed.serializers import AuthorsSerializer
from feed.statuses import GET_POST_SCHEMA_STATUSES, RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES, STATUS_204


class GetPostAuthorsView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['Authors'],
        summary="Get list of authors",
        responses={
            status.HTTP_200_OK: AuthorsSerializer,
            **GET_POST_SCHEMA_STATUSES
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Authors'],
        summary="Create new author",
        responses={
            status.HTTP_201_CREATED: AuthorsSerializer,
            **GET_POST_SCHEMA_STATUSES
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
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Authors'],
        summary="Update author by id",
        responses={
            status.HTTP_200_OK: AuthorsSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=['Authors'],
        summary="Delete author by id",
        responses={
            **STATUS_204,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
