from rest_framework import serializers
from .models import Category, Tag, Post, Comment
from author.serializers import AuthorSerializer

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()

class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()

class RecursiveCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'author_email', 'content', 'created_at', 'replies']

    def get_replies(self, obj):
        if obj.replies.count() > 0:
            return RecursiveCommentSerializer(obj.replies.all(), many=True).data
        return []

class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'author_email', 'content', 'created_at', 'parent_comment', 'replies']

    def validate_author_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError('Email is not valid.')
        return value

    def validate(self, data):
        if data.get('parent_comment'):
            level = 0
            parent = data.get('parent_comment')
            while parent:
                parent = parent.parent_comment
                level += 1
            if level >= 3:
                raise serializers.ValidationError('Max 3 levels allowed for comments.')
        return data

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 'tags', 'created_at', 'updated_at', 'status', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data.get('title', ''))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.slug = slugify(validated_data['title'])
        return super().update(instance, validated_data)
