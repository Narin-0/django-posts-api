from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Модель поста (товара).
    
    Поля:
    - title: Заголовок поста
    - content: Описание/карточка товара
    - created_at: Дата создания
    - author: ForeignKey на пользователя
    """
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',  # Это позволяет получить все посты пользователя через user.posts.all()
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.title} - {self.author.username}'
