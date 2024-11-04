from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from feed.models import Article, Author
from feed.serializers import ArticlesSerializer, ArticleSerializer
from feed.statuses import SCHEMA_PERMISSION_DENIED, GET_POST_SCHEMA_STATUSES, RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES, \
    STATUS_204
from feed.utils import validate_params


class GetArticlesView(generics.ListCreateAPIView):
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        queryset = Article.objects.select_related(
            "author"
        )
        return queryset

    @extend_schema(
        tags=['Articles'],
        summary="Get list of articles",
        responses={
            status.HTTP_200_OK: ArticlesSerializer,
            **GET_POST_SCHEMA_STATUSES

        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostArticleView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=['Articles'],
        summary="Create new article",
        examples=[
            OpenApiExample(
                'Request example',
                {
                    "title": "My first article",
                    "content": "This is my first article",
                },
                request_only=True
            ),
        ],
        responses={
            status.HTTP_201_CREATED: ArticleSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES
        }
    )
    def post(self, request, *args, **kwargs):
        author_id = kwargs.get("author_id")

        title = request.data.get("title")
        content = request.data.get("content")

        dict_for_validate = {
            "author": author_id,
            "title": title,
            "content": content
        }
        error = validate_params(dict_for_validate, "article")
        if error:
            return error

        author = get_object_or_404(Author, pk=author_id)

        data_for_created = {
            "title": title,
            "author": author,
            "content": content,
        }

        Article.objects.create(
            **data_for_created
        )
        return Response(status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyArticleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Article.objects.select_related(
            "author"
        )
        return queryset

    @extend_schema(
        tags=['Articles'],
        summary="Get article by id",
        responses={
            status.HTTP_200_OK: ArticleSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Articles'],
        summary="Update article by id",
        responses={
            status.HTTP_200_OK: ArticleSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        }
    )
    def put(self, request, *args, **kwargs):
        author_id = request.data.get("author")
        get_object_or_404(Author, pk=author_id)
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Articles'],
        summary="Delete article by id",
        responses={
            **STATUS_204,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
