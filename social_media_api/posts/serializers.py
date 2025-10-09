from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


# --- Comment Serializer ---
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


# --- Post List Serializer ---
class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)  # NEW

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'author', 'content',
            'created_at', 'updated_at', 'comment_count', 'like_count'
        ]
        read_only_fields = [
            'id', 'author', 'created_at', 'updated_at',
            'comment_count', 'like_count'
        ]


# --- Post Detail Serializer ---
class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'author', 'content',
            'created_at', 'updated_at', 'comments', 'like_count'
        ]
        read_only_fields = [
            'id', 'author', 'created_at', 'updated_at',
            'comments', 'like_count'
        ]


# --- Like Serializer ---
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
