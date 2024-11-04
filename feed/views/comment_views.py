from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from feed.models import Comment, Author, Article
from feed.serializers import CommentsSerializer
from feed.statuses import SCHEMA_PERMISSION_DENIED, RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES, STATUS_204
from feed.utils import validate_params


def check_parent_comment(article_id, parent_comment):
    error = None
    if parent_comment.article.id != article_id:
        response = {"errors": "The parent comment does not belong to the article"}
        error = Response(response, status=status.HTTP_400_BAD_REQUEST)
    return error


def get_objects(author_id, article_id, parent_comment_id):
    author = get_object_or_404(Author, pk=author_id)
    article = get_object_or_404(Article, pk=article_id)

    parent_comment = None
    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
    return author, article, parent_comment


class GetPostCommentView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        if not article_id:
            return None
        get_object_or_404(Article, pk=article_id)

        queryset = Comment.objects.select_related(
            "article",
            "author",
        ).filter(
            article=article_id,
            parent_comment__isnull=True
        )
        return queryset

    @extend_schema(
        tags=["Comments"],
        summary="Get comments on the article",
        responses={
            status.HTTP_200_OK: CommentsSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED,
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    @extend_schema(
        tags=["Comments"],
        examples=[
            OpenApiExample(
                name="Example of an comment create request",
                value={
                    "comment_text": "Some comment text",
                    "author_id": 1,
                    "parent_comment_id": None
                }
            ),
        ],
        summary="Create comment on the article",
        responses={
            status.HTTP_201_CREATED: CommentsSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED,
        }
    )
    def post(self, request, *args, **kwargs):
        comment_text = request.data.get("comment_text")
        author_id = request.data.get("author_id")
        article_id = kwargs.get("article_id")
        parent_comment_id = request.data.get("parent_comment_id")

        dict_for_validate = {
            "comment_text": comment_text,
            "author_id": author_id,
            "article_id": article_id
        }
        error = validate_params(dict_for_validate, "comment")
        if error:
            return error

        author, article, parent_comment = get_objects(author_id, article_id, parent_comment_id)
        if parent_comment:
            error = check_parent_comment(article_id, parent_comment)
            if error:
                return error

        Comment.objects.create(
            comment_text=comment_text,
            author=author,
            article=article,
            parent_comment=parent_comment
        )
        return Response(status=status.HTTP_201_CREATED)


class UpdateDestroyCommentView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        comment_id = self.kwargs.get("pk")
        if not comment_id:
            return None
        queryset = Comment.objects.select_related(
            "article",
            "author",
        ).filter(
            pk=comment_id
        )
        return queryset

    @extend_schema(
        tags=["Comments"],
        summary="Update comment on the article",
        examples=[
            OpenApiExample(
                name="Example of an comment update request",
                value={
                    "comment_text": "Some comment text",
                    "count_likes": 0,
                    "article": 1,
                    "author": 1,
                    "parent_comment": None
                }
            ),
        ],
        responses={
            status.HTTP_200_OK: CommentsSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED,
        }
    )
    def put(self, request, *args, **kwargs):
        author_id = request.data.get("author")
        article_id = request.data.get("article")
        parent_comment_id = request.data.get("parent_comment")

        _, _, parent_comment = get_objects(author_id, article_id, parent_comment_id)

        if parent_comment_id:
            error = check_parent_comment(article_id, parent_comment)
            if error:
                return error

        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=["Comments"],
        summary="Partial update comment on the article",
        examples=[
            OpenApiExample(
                name="Example of an comment partial update request",
                value={
                    "comment_text": "Some comment text",
                    "count_likes": 0,
                    "article": 1,
                    "author": 1,
                    "parent_comment": None
                }
            ),
        ],
        responses={
            status.HTTP_200_OK: CommentsSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED,
        }
    )
    def patch(self, request, *args, **kwargs):
        author_id = request.data.get("author")
        if author_id:
            get_object_or_404(Author, pk=author_id)

        article_id = request.data.get("article")
        if article_id:
            get_object_or_404(Article, pk=article_id)

        parent_comment_id = request.data.get("parent_comment")

        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
            error = check_parent_comment(article_id, parent_comment)
            if error:
                return error

        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["Comments"],
        summary="Delete comment on the article",
        responses={
            **STATUS_204,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED,
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
