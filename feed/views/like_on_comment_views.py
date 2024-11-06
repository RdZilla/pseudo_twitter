from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from feed.models import LikeOnComment, Author, Comment
from feed.serializers import LikeOnCommentSerializer
from feed.statuses import SCHEMA_PERMISSION_DENIED, SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES, STATUS_204
from feed.utils import validate_params


class LikeOnCommentView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LikeOnCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        parameters=[
            OpenApiParameter(
                "current_user_like",
                type={"type": "bool"}, required=False, enum=["true", "false"]
            )
        ],

        responses={
            status.HTTP_200_OK: LikeOnCommentSerializer,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES
        },
    )
    def get(self, request, *args, **kwargs):
        current_user_like = request.query_params.get("current_user_like")
        dict_for_validate = {
            "current_user_like": current_user_like
        }
        error = validate_params(dict_for_validate, "LikeOnComment")
        if error:
            return error

        current_user_like = current_user_like.lower() == "true"
        if current_user_like:
            return super().retrieve(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                name="Example of a like on comment create request",
                value={
                    "reaction": "&#128077;"
                }
            ),
        ],
        responses={
            status.HTTP_201_CREATED: status.HTTP_201_CREATED,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Create like on comment"
    )
    def post(self, request, *args, **kwargs):
        author_id = request.user.id

        comment_id = kwargs.get("comment_id")
        reaction = request.data.get("reaction")
        dict_for_validate = {
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

    def get_object(self):
        author_id = self.request.user.id

        comment_id = self.kwargs['comment_id']
        if not comment_id or not author_id:
            return None

        get_object_or_404(Comment, pk=comment_id)

        qs = get_object_or_404(LikeOnComment, comment_id=comment_id, author_id=author_id)
        return qs

    @extend_schema(
        examples=[
            OpenApiExample(
                name="Example of a like on comment update request",
                value={
                    "reaction": "&#128077;"
                }
            ),
        ],
        responses={
            status.HTTP_200_OK: LikeOnCommentSerializer,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Update like on comment"
    )
    def put(self, request, *args, **kwargs):
        self.get_object()
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
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Partial update like on comment"
    )
    def patch(self, request, *args, **kwargs):
        self.get_object()
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        responses={
            **STATUS_204,
            **SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES,
            **SCHEMA_PERMISSION_DENIED
        },
        tags=["Likes"],
        summary="Delete like on comment"
    )
    def delete(self, request, *args, **kwargs):
        self.get_object()
        comment_id = kwargs["comment_id"]
        comment = Comment.objects.get(id=comment_id)
        comment.count_of_likes -= 1
        comment.save()
        return super().delete(request, *args, **kwargs)

    @staticmethod
    def get_objects(author_id, comment_id):
        author = get_object_or_404(Author, pk=author_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        return author, comment
