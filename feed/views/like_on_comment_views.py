from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from feed.models import LikeOnComment, Author, Comment
from feed.serializers import LikeOnCommentSerializer
from feed.statuses import SCHEMA_PERMISSION_DENIED, RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES, STATUS_204
from feed.utils import validate_params


class GetPostLikeOnComment(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeOnCommentSerializer

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        if not comment_id:
            return None
        get_object_or_404(Comment, pk=comment_id)
        qs = LikeOnComment.objects.select_related(
            'author',
            'comment'
        ).filter(
            comment=comment_id
        )
        return qs

    @extend_schema(
        tags=["Likes"],
        summary="Get like on comment",
        responses={
            status.HTTP_200_OK: LikeOnCommentSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                name="Example of a like on comment create request",
                value={
                    "author_id": 1,
                    "reaction": "&#128077;"
                }
            ),
        ],
        responses={
            status.HTTP_201_CREATED: status.HTTP_201_CREATED,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Create like on comment"
    )
    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")
        author_id = request.data.get("author_id")
        reaction = request.data.get("reaction")
        dict_for_validate = {
            "author_id": author_id,
            "comment_id": comment_id,
            "reaction": reaction
        }
        error = validate_params(dict_for_validate, "like")
        if error:
            return error

        author, comment = self.get_objects(author_id, comment_id)
        try:
            LikeOnComment.objects.create(
                author=author,
                reaction=reaction,
                comment=comment
            )
            comment.count_of_likes += 1
            comment.save()
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            response = Response({"errors": "Unique constraint failed."}, status=status.HTTP_400_BAD_REQUEST)
            return response

    @staticmethod
    def get_objects(author_id, comment_id):
        author = get_object_or_404(Author, pk=author_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        return author, comment


class RetrieveUpdateDestroyLikeOnCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LikeOnCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'comment_id'
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        author_id = self.kwargs['author_id']
        if not comment_id or not author_id:
            return None

        get_object_or_404(Author, pk=author_id)
        get_object_or_404(Comment, pk=comment_id)
        qs = LikeOnComment.objects.select_related(
            'author', 'comment'
        ).filter(
            author=author_id,
            comment=comment_id
        )
        return qs

    @extend_schema(
        responses={
            status.HTTP_200_OK: LikeOnCommentSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Get like on comment"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                name="Example of a like on comment update request",
                value={
                    "author_id": 1,
                    "reaction": "&#128077;"
                }
            ),
        ],
        responses={
            status.HTTP_200_OK: LikeOnCommentSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Update like on comment"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                name="Example of a like on comment partial update request",
                value={
                    "reaction": "&#128077;"
                }
            ),
        ],
        responses={
            status.HTTP_200_OK: LikeOnCommentSerializer,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Partial update like on comment"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        responses={
            **STATUS_204,
            **RETRIEVE_UPDATE_DESTROY_SCHEMA_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Delete like on comment"
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
