from django.urls import path

from .views.author_views import GetPostAuthorsView, RetrieveUpdateDestroyAuthorView
from .views.article_views import GetArticlesView, PostArticleView, RetrieveUpdateDestroyArticleView
from .views.comment_views import GetPostCommentView, UpdateDestroyCommentView
from .views.like_on_comment_views import GetPostLikeOnComment, RetrieveUpdateDestroyLikeOnCommentView

urlpatterns = [
    # Authors
    path("author/", GetPostAuthorsView.as_view(), name="list_authors_create_author"),
    path("author/<str:pk>/", RetrieveUpdateDestroyAuthorView.as_view(), name="retrieve_author"),

    # Articles
    path("article/", GetArticlesView.as_view(), name="list_articles"),
    path("author/<str:author_id>/article/", PostArticleView.as_view(), name="create_article"),
    path("article/<str:pk>/", RetrieveUpdateDestroyArticleView.as_view(), name="retrieve_update_destroy_article"),

    # Comments
    path("articles/<str:article_id>/comments/", GetPostCommentView.as_view(), name="list_comments"),
    path("comments/<str:pk>/", UpdateDestroyCommentView.as_view(), name="create_comment"),

    # Likes on Comments
    path("comment/<str:comment_id>/like/", GetPostLikeOnComment.as_view(), name="list_likes_create_like_on_comment"),
    path("comment/<str:comment_id>/like/<str:author_id>/", RetrieveUpdateDestroyLikeOnCommentView.as_view(),
         name="delete_like_on_comment"),
]
