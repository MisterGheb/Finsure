from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db.models import F
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import ScopedRateThrottle


@api_view(['GET'])
@throttle_classes([ScopedRateThrottle])
def get_all_blog_posts(request):
    """
    List all blog posts, with optional filtering and pagination.

    Query params:
      - ?author=...      # case-insensitive substring match
      - ?title=...       # case-insensitive substring match
      - ?category=...    # exact choice-value match
      - ?page=...        # which page to retrieve (1-based)
      - ?page_size=...   # optional override per-page size (max 100)
    """
    qs = BlogPost.objects.all()

    # --- filtering ---
    author = request.query_params.get('author')
    title  = request.query_params.get('title')
    category = request.query_params.get('category')

    if author:
        qs = qs.filter(author__icontains=author)
    if title:
        qs = qs.filter(title__icontains=title)
    if category:
        qs = qs.filter(category=category)

    # --- pagination ---
    paginator = PageNumberPagination()
    paginator.page_size = 10                  # default page size
    paginator.page_size_query_param = 'page_size'
    paginator.max_page_size = 100

    page = paginator.paginate_queryset(qs, request)
    serializer = BlogPostSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)
get_all_blog_posts.throttle_scope = 'posts'

@api_view(['GET'])
@throttle_classes([ScopedRateThrottle])
def get_blog_post(request, pk):
    """
    Retrieve a single blog post by its ID.
    """
    post = get_object_or_404(BlogPost, pk=pk)
    serializer = BlogPostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
def create_blog_post(request):
    """
    Create a new blog post.
    """
    serializer = BlogPostSerializer(data=request.data)
    if serializer.is_valid():

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_blog_post(request, pk):
    """
    Update an existing blog post.
    """
    post = get_object_or_404(BlogPost, pk=pk)
    serializer = BlogPostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_blog_post(request, pk):
    """
    Delete a blog post.
    """
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@throttle_classes([ScopedRateThrottle])
def vote_blog_post(request, pk):
    """
    Increment the likes count if {"like": true} is sent,
    or increment the dislikes count if {"like": false} is sent.
    Returns the updated totals.
    """
    post = get_object_or_404(BlogPost, pk=pk)
    flag = request.data.get('like', None)

    # Normalize JSON booleans vs. strings
    is_like = flag is True or str(flag).lower() == 'true'
    is_dislike = flag is False or str(flag).lower() == 'false'

    if is_like:
        # Atomic increment in the database
        BlogPost.objects.filter(pk=pk).update(likes=F('likes') + 1)
        # Refresh from DB so post.likes is up to date
        post.refresh_from_db(fields=['likes'])
    elif is_dislike:
        BlogPost.objects.filter(pk=pk).update(dislikes=F('dislikes') + 1)
        post.refresh_from_db(fields=['dislikes'])
    else:
        return Response(
            {"error": "`like` must be true or false."},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {"likes": post.likes, "dislikes": post.dislikes},
        status=status.HTTP_200_OK
    )
vote_blog_post.throttle_scope = 'votes'

@api_view(['GET'])
@throttle_classes([ScopedRateThrottle])
def get_comments(request, post_id):
    """
    List all comments for a specific blog post.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
get_comments.throttle_scope = 'posts'

@api_view(['POST'])
@throttle_classes([ScopedRateThrottle])
def create_comment(request, post_id):
    """
    Create a new comment for a specific blog post.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
create_comment.throttle_scope = 'posts'

@api_view(['PUT'])
@throttle_classes([ScopedRateThrottle])
def update_comment(request, post_id, comment_id):
    """
    Update an existing comment for a specific blog post.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_comment(request, post_id, comment_id):
    """
    Delete a comment for a specific blog post.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_specific_blog_comment(request, post_id, comment_id):
    """
    Retrieve a specific comment for a specific blog post.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)


@api_view(['GET'])
@throttle_classes([ScopedRateThrottle])
def get_blog_post_by_title_or_author(request, title, author):
    """
    Retrieve a blog post by its title and author.
    """
    if not title or not author:
        return Response({"error": "Title and author are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not isinstance(title, str) or not isinstance(author, str):
        return Response({"error": "Title and author must be strings."}, status=status.HTTP_400_BAD_REQUEST)
    
    if title and author:
        post = get_object_or_404(BlogPost, title=title, author=author)
    elif author:
        post = get_object_or_404(BlogPost, author=author)
    elif title:
        post = get_object_or_404(BlogPost, title=title)
    serializer = BlogPostSerializer(post)
    return Response(serializer.data)