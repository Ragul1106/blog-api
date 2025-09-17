from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializerV1, BlogSerializerV2
from rest_framework.throttling import UserRateThrottle

class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return BlogSerializerV1
        return BlogSerializerV2

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
