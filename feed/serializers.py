from rest_framework import serializers

from feed.models import Article, Author, Comment, LikeOnComment


class GetAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GetArticlesSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["id", "title", "author", "create_date"]

    def get_author(self, obj):
        author_fullname = None
        if obj.author:
            author_fullname = obj.author.full_name
        return author_fullname


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    child_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_author(self, obj):
        author_fullname = None
        if obj.author:
            author_fullname = obj.author.full_name
        return author_fullname

    def get_child_comments(self, obj):
        child_comments = Comment.objects.filter(parent_comment=obj.id)
        if child_comments:
            return CommentsSerializer(child_comments, many=True).data
        return None


class LikeOnCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = LikeOnComment
        fields = ["id", "author", "reaction", "create_date"]

    def get_author(self, obj):
        author_fullname = None
        if obj.author:
            author_fullname = obj.author.full_name
        return author_fullname
