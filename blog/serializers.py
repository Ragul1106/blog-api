from rest_framework import serializers
from .models import Blog

# v1: title + content
class BlogSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content']

# v2: adds category, tags, view_count
class BlogSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'category', 'tags', 'view_count']
        read_only_fields = ['view_count']  # view_count auto-increment
