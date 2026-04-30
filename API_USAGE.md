# 🚀 API READY - Django REST Framework Posts Application

## 📌 Status: ✅ Running

Сервер успешно запущен на **http://127.0.0.1:8000/**

### Учётные данные для тестирования:

```
Admin:
  username: admin
  password: admin123456
  
User (ivan):
  username: ivan
  password: test123456
  email: ivan@example.com
```

---

## 🌐 API Endpoints

### Интерактивный API (Browsable API)
- **http://127.0.0.1:8000/api/** - Главная страница API
- **http://127.0.0.1:8000/api/users/** - Список пользователей
- **http://127.0.0.1:8000/api/posts/** - Список постов
- **http://127.0.0.1:8000/admin/** - Django Admin

---

## 📋 Примеры запросов

### 1. Получить всех пользователей с их постами

```bash
curl -X GET http://127.0.0.1:8000/api/users/ \
  -H "Accept: application/json"
```

**Ответ:**
```json
{
    "count": 2,
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
                    "content": "Описание первого товара с картинкой",
                    "author": {
                        "id": 1,
                        "username": "ivan",
                        "email": "ivan@example.com",
                        "first_name": "Иван",
                        "last_name": "Сидоров"
                    },
                    "created_at": "2026-04-30T07:34:55Z"
                },
                {
                    "id": 2,
                    "title": "Товар 2",
                    "content": "Описание второго товара",
                    "author": {
                        "id": 1,
                        "username": "ivan",
                        "email": "ivan@example.com",
                        "first_name": "Иван",
                        "last_name": "Сидоров"
                    },
                    "created_at": "2026-04-30T07:34:55Z"
                }
            ]
        }
    ]
}
```

### 2. Получить одного пользователя по ID

```bash
curl -X GET http://127.0.0.1:8000/api/users/1/ \
  -H "Accept: application/json"
```

### 3. Получить все посты этого пользователя (custom action)

```bash
curl -X GET http://127.0.0.1:8000/api/users/1/posts/ \
  -H "Accept: application/json"
```

### 4. Получить список всех постов

```bash
curl -X GET http://127.0.0.1:8000/api/posts/ \
  -H "Accept: application/json"
```

### 5. Получить конкретный пост по ID

```bash
curl -X GET http://127.0.0.1:8000/api/posts/1/ \
  -H "Accept: application/json"
```

### 6. Создать новый пост (требуется аутентификация)

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "title": "Новый товар",
    "content": "Описание нового товара"
  }'
```

Или используя Basic Auth (Session Authentication):

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -u ivan:test123456 \
  -d '{
    "title": "Ещё один товар",
    "content": "Описание ещё одного товара"
  }'
```

### 7. Обновить пост

```bash
curl -X PUT http://127.0.0.1:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -u ivan:test123456 \
  -d '{
    "title": "Обновленный товар",
    "content": "Обновленное описание"
  }'
```

### 8. Удалить пост

```bash
curl -X DELETE http://127.0.0.1:8000/api/posts/1/ \
  -u ivan:test123456
```

### 9. Получить Token (для Token Authentication)

```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan",
    "password": "test123456"
  }'
```

---

## 🔑 Ключевые особенности реализации

### 1️⃣ Nested Serializers

**UserSerializer** содержит массив постов:
```python
class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
```

**PostSerializer** содержит полную информацию об авторе:
```python
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'email': obj.author.email,
            ...
        }
```

### 2️⃣ Related Name

В модели `Post`:
```python
author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='posts',  # ← Это позволяет user.posts.all()
)
```

### 3️⃣ Автоматическое назначение автора

При создании поста текущий пользователь назначается автором:
```python
def perform_create(self, serializer):
    serializer.save(author=self.request.user)
```

### 4️⃣ ViewSets и Router

Автоматическая генерация всех CRUD операций:
```python
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
```

---

## 📁 Структура проекта

```
/home/narin_0/Documents/123456/
├── config/
│   ├── settings.py          # Django конфигурация
│   ├── urls.py              # URL роуты
│   ├── wsgi.py
│   └── asgi.py
├── posts/
│   ├── models.py            # Post и User моделис
│   ├── serializers.py       # Nested serializers
│   ├── views.py             # ViewSets
│   ├── admin.py             # Django Admin
│   └── migrations/
├── venv/                    # Виртуальное окружение
├── manage.py
├── db.sqlite3               # База данных
├── requirements.txt
└── README.md
```

---

## 🛠️ Полезные команды

```bash
# Активировать виртуальное окружение
source venv/bin/activate

# Запустить сервер
python manage.py runserver

# Создать новую миграцию
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Интерпретатор Django
python manage.py shell

# Запустить тесты
python manage.py test

# Собрать статические файлы
python manage.py collectstatic
```

---

## 🔐 Permissions & Authentication

- **IsAuthenticatedOrReadOnly** - Любой может читать, только авторизованные могут писать
- **Token Authentication** - Поддерживается
- **Session Authentication** - Поддерживается (для браузера)

---

## 📝 Тестовые данные

База данных уже содержит:
- ✅ 2 пользователя (ivan, admin)
- ✅ 2 поста от пользователя ivan

---

## 🐛 Troubleshooting

### Если сервер не запускается:
```bash
# Убедитесь что виртуальное окружение активировано
source venv/bin/activate

# Проверьте зависимости
pip install -r requirements.txt

# Запустите миграции
python manage.py migrate
```

### Если порт 8000 уже занят:
```bash
python manage.py runserver 0.0.0.0:8080
```

### Если нужно пересоздать БД:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📞 Документация

- [Django Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [README.md](README.md) - Полная документация проекта

---

**Дата создания:** 30 апреля 2026  
**Версия Django:** 4.2.13  
**Версия DRF:** 3.14.0  
**Python:** 3.14.3
