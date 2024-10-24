from django.urls import path

from feed.views import GetArticlesView, GetArticleView, GetAuthorsView, GetCommentView, PostArticleView, \
    PostCommentView, PostLikeOnComment, GetLikesOnComment, DeleteLikeOnComment

urlpatterns = [
    path("get_authors", GetAuthorsView.as_view(), name="get_authors"),
    path("get_articles", GetArticlesView.as_view(), name="get_articles"),
    path("get_article/<str:pk>", GetArticleView.as_view(), name="get_articles"),
    path("post_article", PostArticleView.as_view(), name="post_article"),
    path("get_comments/<str:article_id>", GetCommentView.as_view(), name="get_comments"),
    path("post_comment", PostCommentView.as_view(), name="post_comment"),
    path("get_likes_on_comment/<str:comment_id>", GetLikesOnComment.as_view(), name="get_like_on_comment"),
    path("post_like_on_comment", PostLikeOnComment.as_view(), name="post_like_on_comment"),
    path("delete_like_on_comment/<str:author_id>/<str:comment_id>", DeleteLikeOnComment.as_view(),
         name="delete_like_on_comment")
]
