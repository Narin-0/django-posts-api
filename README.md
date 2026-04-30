# Django REST API - Posts Application

Полноценное REST API приложение на Django + Django REST Framework с nested serializers для управления пользователями и постами.

## Структура проекта

```
.
├── config/                  # Основная конфигурация Django
│   ├── settings.py         # Настройки Django
│   ├── urls.py             # Main URL patterns
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
├── posts/                   # Django приложение
│   ├── models.py           # Модели Post и User
│   ├── serializers.py      # Nested serializers
│   ├── views.py            # ViewSets для CRUD
│   ├── urls.py             # URL patterns приложения
│   ├── admin.py            # Django Admin
│   ├── apps.py
│   └── tests.py
├── manage.py               # Django management command
└── requirements.txt        # Python зависимости
```

## Установка

### 1. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Миграции БД

```bash
python manage.py migrate
```

### 4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

Сервер запустится на `http://127.0.0.1:8000/`

## API Endpoints

### Пользователи (Users)

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/api/users/` | Список всех пользователей со своими постами |
| GET | `/api/users/{id}/` | Получить пользователя с его постами |
| POST | `/api/users/` | Создать нового пользователя |
| PUT | `/api/users/{id}/` | Обновить пользователя |
| DELETE | `/api/users/{id}/` | Удалить пользователя |
| GET | `/api/users/{id}/posts/` | Получить все посты пользователя |

### Посты (Posts)

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/api/posts/` | Список всех постов с полной инфо об авторах |
| GET | `/api/posts/{id}/` | Получить конкретный пост |
| POST | `/api/posts/` | Создать новый пост |
| PUT | `/api/posts/{id}/` | Обновить пост |
| DELETE | `/api/posts/{id}/` | Удалить пост |

## Примеры использования

### 1. Получение списка пользователей с постами

```bash
curl -X GET http://127.0.0.1:8000/api/users/
```

**Ответ:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "ivan",
            "email": "ivan@example.com",
            "first_name": "Иван",
            "last_name": "Сидоров",
            "posts": [
                {
                    "id": 1,
                    "title": "Товар 1",
                    "content": "Описание товара 1",
                    "author": {
                        "id": 1,
                        "username": "ivan",
                        "email": "ivan@example.com",
                        "first_name": "Иван",
                        "last_name": "Сидоров"
                    },
                    "created_at": "2024-04-30T10:30:00Z"
                }
            ]
        }
    ]
}
```

### 2. Создание нового поста

Требуется аутентификация!

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "title": "Новый товар",
    "content": "Описание нового товара"
  }'
```

**Ответ:**
```json
{
    "id": 2,
    "title": "Новый товар",
    "content": "Описание нового товара",
    "author": {
        "id": 1,
        "username": "ivan",
        "email": "ivan@example.com",
        "first_name": "Иван",
        "last_name": "Сидоров"
    },
    "created_at": "2024-04-30T11:00:00Z"
}
```

### 3. Получение постов конкретного пользователя

```bash
curl -X GET http://127.0.0.1:8000/api/users/1/posts/
```

**Ответ:**
```json
[
    {
        "id": 1,
        "title": "Товар 1",
        "content": "Описание товара 1",
        "author": {
            "id": 1,
            "username": "ivan",
            "email": "ivan@example.com",
            "first_name": "Иван",
            "last_name": "Сидоров"
        },
        "created_at": "2024-04-30T10:30:00Z"
    }
]
```

## Ключевые особенности

### 1. **Nested Serializers**

```python
class UserSerializer(serializers.ModelSerializer):
    # Posts получаются через related_name='posts' из модели
    posts = PostSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'posts']
```

```python
class PostSerializer(serializers.ModelSerializer):
    # Author включает полную информацию пользователя
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'email': obj.author.email,
            ...
        }
```

### 2. **Related Name**

В модели Post используется `related_name='posts'`:

```python
author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='posts',  # Позволяет обращаться как user.posts.all()
)
```

Это позволяет:
- Получить все посты пользователя: `user.posts.all()`
- Использовать в ORM: `User.objects.prefetch_related('posts')`
- Получить в сериализаторе через source: `posts = PostSerializer(source='posts', many=True)`

### 3. **Автоматическое назначение автора**

При создании поста, текущий пользователь автоматически назначается автором:

```python
def perform_create(self, serializer):
    serializer.save(author=self.request.user)
```

### 4. **ViewSets и Router**

ViewSets автоматически генерируют URL patterns:

```python
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

Это создаёт:
- `/api/users/` - List
- `/api/users/{id}/` - Retrieve, Update, Delete
- `/api/posts/` - List, Create
- И многое другое...

## Модели

### Post Model

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
```

### User Model

Используется встроенная модель Django: `django.contrib.auth.models.User`

## Permissions & Authentication

- `IsAuthenticatedOrReadOnly` - Любой может читать, только авторизованные могут создавать/редактировать
- Поддерживает Token Authentication и Session Authentication

## Настройки DRF

В `config/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

## Администрирование

Доступно на `/admin/` с суперпользователем.

Настроено:
- Список постов с фильтрацией по автору и дате
- Поиск по названию, содержимому и имени автора
- Красивое отображение всех полей

## Возможные расширения

1. **Фильтрация и поиск**
   ```python
   from rest_framework.filters import SearchFilter, OrderingFilter
   ```

2. **Пагинация**
   - Уже настроена в settings.py

3. **Кэширование**
   - Использовать Django cache framework

4. **Rate limiting**
   - Ограничение количества запросов

5. **Документация API**
   - Установить `drf-spectacular` для Swagger/OpenAPI

## Тестирование

```bash
python manage.py test
```

## Лицензия

MIT

---

**Автор:** Your Name  
**Дата:** 2024
