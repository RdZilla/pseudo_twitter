from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from rest_framework import generics, serializers, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from feed.models import Article, Author, Comment, LikeOnComment
from feed.serializers import GetArticlesSerializer, GetAuthorsSerializer, CommentsSerializer, ArticleSerializer, \
    LikeOnCommentSerializer

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
    ),
}


@extend_schema(
    tags=['Articles'],
    summary="Get list of authors",
    responses={
        200: GetAuthorsSerializer,
        400: inline_serializer(
            "GetAuthors400",
            {
                "errors": serializers.CharField()
            }
        )
    }
)
class GetAuthorsView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = GetAuthorsSerializer


@extend_schema(
    tags=['Articles'],
    summary="Get list of articles",
    responses={
        200: GetArticlesSerializer,
        400: inline_serializer(
            "GetArticles400",
            {
                "errors": serializers.CharField()
            }
        )
    }
)
class GetArticlesView(generics.ListAPIView):
    serializer_class = GetArticlesSerializer

    def get_queryset(self):
        queryset = Article.objects.select_related(
            "author"
        ).all()
        return queryset


@extend_schema(
    tags=['Articles'],
    summary="Get article by id",
    responses={
        200: ArticleSerializer,
        400: inline_serializer(
            "GetArticle400",
            {
                "errors": serializers.CharField()
            }
        ),
        **SCHEMA_PERMISSION_DENIED
    }
)
class GetArticleView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.select_related(
            "author"
        )
        return queryset


@extend_schema(
    examples=[
        OpenApiExample(
            "Post example",
            description="Create article",
            value={
                "title": "string",
                "content": "string",
                "author_id": 1}
        ),
    ],
    responses={
        201: status.HTTP_201_CREATED,
        400: inline_serializer(
            "PostArticle400",
            {
                "errors": serializers.CharField()
            }
        ),
        404: inline_serializer(
            "Not Found",
            {
                "errors": serializers.CharField(default="No Author matches the given query."),
            }
        ),
        **SCHEMA_PERMISSION_DENIED
    },
    tags=["Articles"],
    summary="Create article"
)
class PostArticleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSerializer

    def post(self, request, *args, **kwargs):
        post_data = request.data
        title = post_data.get("title")
        content = post_data.get("content")
        author_id = post_data.get("author_id")

        error = self.validate_data(title, content, author_id)
        if error:
            return error

        author = get_object_or_404(Author, pk=author_id)

        Article.objects.create(
            title=title,
            content=content,
            author=author
        )
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_data(title, content, author_id):
        if not title:
            response = {"errors": "The title of the article is missing."}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error

        if not content:
            response = {"errors": "The content of the article is missing."}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error

        if not author_id:
            response = {"errors": "The author of the article is missing"}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error
        return None


@extend_schema(
    tags=['Articles'],
    summary="Get comments on the article",
    responses={
        200: CommentsSerializer,
        400: inline_serializer(
            "GetComment400",
            {
                "errors": serializers.CharField()
            }
        )
    }
)
class GetCommentView(generics.ListAPIView):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        if not article_id:
            return None

        queryset = Comment.objects.select_related(
            "article",
            "author",
        ).filter(
            article=article_id, parent_comment__isnull=True
        )
        return queryset


@extend_schema(
    examples=[
        OpenApiExample(
            "Post example",
            description="Create comment on article",
            value={
                "comment_text": "string",
                "author_id": 1,
                "article_id": 1,
                "parent_comment_id": None
            }
        ),
    ],
    responses={
        201: status.HTTP_201_CREATED,
        400: inline_serializer(
            "PostComment400",
            {
                "errors": serializers.CharField()
            }
        ),
        404: inline_serializer(
            "Not Found",
            {
                "errors": serializers.CharField(default="No Author matches the given query."),
            }
        ),
        **SCHEMA_PERMISSION_DENIED
    },
    tags=["Articles"],
    summary="Create comment on article"
)
class PostCommentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentsSerializer

    def post(self, request, *args, **kwargs):
        post_data = request.data
        comment_text = post_data.get("comment_text")
        author_id = post_data.get("author_id")
        article_id = post_data.get("article_id")
        parent_comment_id = post_data.get("parent_comment_id")

        error = self.validate_data(comment_text, author_id, article_id)
        if error:
            return error

        author, article, parent_comment = self.get_objects(author_id, article_id, parent_comment_id)

        Comment.objects.create(
            comment_text=comment_text,
            author=author,
            article=article,
            parent_comment=parent_comment
        )
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_data(comment_text, author_id, article_id):
        if not comment_text:
            response = {"errors": "The text of the comment is missing."}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error

        if not author_id:
            response = {"errors": "The author of the comment is missing"}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error

        if not article_id:
            response = {"errors": "The article of the comment is missing"}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error
        return None

    @staticmethod
    def get_objects(author_id, article_id, parent_comment_id):
        author = get_object_or_404(Author, pk=author_id)
        article = get_object_or_404(Article, pk=article_id)

        parent_comment = None
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
        return author, article, parent_comment


@extend_schema(
    tags=["Articles"],
    summary="Get likes on comment"
)
class GetLikesOnComment(generics.ListAPIView):
    serializer_class = LikeOnCommentSerializer

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_id")
        if not comment_id:
            return None

        queryset = LikeOnComment.objects.select_related(
            "author",
            "comment"
        ).filter(
            comment=comment_id
        )
        return queryset


@extend_schema(
    examples=[
        OpenApiExample(
            "Post example",
            description="Create like on comment",
            value={
                "author_id": 1,
                "comment_id": 1,
                "reaction": "string"
            }
        ),
    ],
    responses={
        201: status.HTTP_201_CREATED,
        400: inline_serializer(
            "PostComment400",
            {
                "errors": serializers.CharField()
            }
        ),
        404: inline_serializer(
            "Not Found",
            {
                "errors": serializers.CharField(default="No Author matches the given query."),
            }
        ),
        **SCHEMA_PERMISSION_DENIED
    },
    tags=["Articles"],
    summary="Create like on comment"
)
class PostLikeOnComment(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeOnCommentSerializer

    def post(self, request, *args, **kwargs):
        post_data = request.data
        author_id = post_data.get("author_id")
        comment_id = post_data.get("comment_id")
        reaction = post_data.get("reaction")

        error = self.validate_data(author_id, comment_id, reaction)
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

    @staticmethod
    def validate_data(author_id, comment_id, reaction):
        if not author_id:
            response = {"errors": "The author of the like is missing"}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error

        if not comment_id:
            response = {"errors": "The comment of the like is missing"}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error

        if not reaction:
            response = {"errors": "The reaction of the like is missing"}
            error = Response(response, status=status.HTTP_400_BAD_REQUEST)
            return error
        return None


@extend_schema(
    responses={
        204: status.HTTP_204_NO_CONTENT,
        400: inline_serializer(
            "DeleteComment400",
            {
                "errors": serializers.CharField()
            }
        ),
        404: inline_serializer(
            "Not Found",
            {
                "errors": serializers.CharField(default="No Author matches the given query."),
            }
        ),
        **SCHEMA_PERMISSION_DENIED
    },
    tags=["Articles"],
    summary="Delete like on comment"
)
class DeleteLikeOnComment(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = LikeOnComment
    serializer_class = LikeOnCommentSerializer

    def get_object(self):
        author_id = self.kwargs['author_id']
        comment_id = self.kwargs['comment_id']

        like_on_comment = LikeOnComment.objects.filter(author=author_id, comment=comment_id)
        return like_on_comment
