from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Post с полной информацией об авторе.
    
    Включает nested serializer для автора поста,
    чтобы в ответе была вся информация об авторе, а не просто его ID.
    """
    # Вложенный сериализатор для автора - показываем полную информацию
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'created_at', 'author']

    def get_author(self, obj):
        """
        Возвращает полную информацию об авторе поста.
        """
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'email': obj.author.email,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для User с nested постами.
    
    Включает все посты пользователя благодаря related_name='posts' в модели Post.
    """
    # Posts с related_name из модели - все посты этого пользователя
    posts = PostSerializer(many=True, read_only=True, source='posts')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'posts']
        read_only_fields = ['id', 'posts']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового пользователя.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        """
        Создаёт нового пользователя с хешированным паролем.
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(
            **validated_data,
            password=password
        )
        return user


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания поста.
    Автор назначается автоматически из текущего пользователя.
    """
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']
