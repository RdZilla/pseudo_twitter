from rest_framework import serializers

from feed.models import Article, Author, Comment, LikeOnComment


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ArticlesSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["id", "title", "author", "create_date"]

    @staticmethod
    def get_author(obj):
        author_fullname = None
        if obj.author:
            author_fullname = obj.author.full_name
        return author_fullname


class ArticleSerializer(serializers.ModelSerializer):
    author_fullname = serializers.SerializerMethodField()
    is_updated = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = "__all__"

    @staticmethod
    def get_author_fullname(obj):
        author_fullname = None
        if obj.author:
            author_fullname = obj.author.full_name
        return author_fullname

    @staticmethod
    def get_is_updated(obj):
        create_date = obj.create_date
        update_date = obj.update_date
        return create_date != update_date


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_updated = serializers.SerializerMethodField()
    child_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    @staticmethod
    def get_author(obj):
        author_fullname = None
        if obj.author:
            author_fullname = obj.author.full_name
        return author_fullname

    @staticmethod
    def get_is_updated(obj):
        create_date = obj.create_date
        update_date = obj.update_date
        return create_date != update_date

    @staticmethod
    def get_child_comments(obj):
        child_comments = Comment.objects.filter(parent_comment=obj.id)
        if child_comments:
            return CommentsSerializer(child_comments, many=True).data
        return None


class LikeOnCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = LikeOnComment
        fields = ["id", "author", "reaction", "create_date"]

    @staticmethod
    def get_author(obj):
        author_fullname = None
        if obj.author:
            author_fullname = obj.author.full_name
        return author_fullname
