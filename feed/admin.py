from django.contrib import admin

from feed.models import Article, Author, Comment, LikeOnComment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "create_date"]
    search_fields = ["title", "author"]
    list_select_related = ["author"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "registration_date"]
    search_fields = ["full_name"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["create_date", "author", "article", "comment_text"]
    search_fields = ["author", "comment_text"]
    list_select_related = ["author", "article", "parent_comment"]


@admin.register(LikeOnComment)
class LikeOnCommentAdmin(admin.ModelAdmin):
    list_display = ["comment", "author", "reaction", "create_date"]
    list_select_related = ["author", "comment"]
