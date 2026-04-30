from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Post
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    PostSerializer,
    PostCreateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.
    
    Endpoints:
    - GET /api/users/ - получить список всех пользователей с их постами
    - GET /api/users/{id}/ - получить пользователя с его постами
    - POST /api/users/ - создать нового пользователя
    - PUT /api/users/{id}/ - обновить пользователя
    - DELETE /api/users/{id}/ - удалить пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        Использует разные сериализаторы для создания и получения.
        """
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """
        Custom action для получения всех постов конкретного пользователя.
        GET /api/users/{id}/posts/
        """
        user = self.get_object()
        posts = user.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления постами.
    
    Endpoints:
    - GET /api/posts/ - получить список всех постов с информацией об авторах
    - GET /api/posts/{id}/ - получить конкретный пост с информацией об авторе
    - POST /api/posts/ - создать новый пост (автор назначается автоматически)
    - PUT /api/posts/{id}/ - обновить пост
    - DELETE /api/posts/{id}/ - удалить пост
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        Использует разные сериализаторы для создания и получения.
        """
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """
        Автоматически назначает текущего пользователя автором при создании поста.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Обновляет пост, сохраняя оригинального автора.
        """
        serializer.save(author=self.request.user)
