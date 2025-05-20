# blog_posts/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Posts
    path('posts/',                  get_all_blog_posts,   name='post-list'),
    path('posts/create/',           create_blog_post,    name='post-create'),
    path('posts/<int:pk>/',         get_blog_post,       name='post-detail'),
    path('posts/<int:pk>/update/',  update_blog_post,    name='post-update'),
    path('posts/<int:pk>/delete/',  delete_blog_post,    name='post-delete'),
    path('posts/<int:pk>/vote/',   vote_blog_post,      name='post-like'),

    # Comments (nested under posts)
    path('posts/<int:post_id>/comments/',                    get_comments,               name='comment-list'),
    path('posts/<int:post_id>/comments/create/',             create_comment,             name='comment-create'),
    path('posts/<int:post_id>/comments/<int:comment_id>/',   get_specific_blog_comment,  name='comment-detail'),
    path('posts/<int:post_id>/comments/<int:comment_id>/update/', update_comment,         name='comment-update'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', delete_comment,         name='comment-delete'),
]
