from rest_framework import serializers
from .models import BlogPost, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'content',
            'author', 'category',
            'likes', 'dislikes',
            'created_at', 'updated_at',
            'comments',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes', 'dislikes']