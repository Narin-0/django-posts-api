#!/bin/bash

# Django REST API Testing Script
# API: http://127.0.0.1:8000/api/

BASE_URL="http://127.0.0.1:8000/api"
USER="ivan"
PASS="test123456"

echo "================================"
echo "🚀 Django REST API Test Suite"
echo "================================"

# 1. Get all users with their posts
echo -e "\n\n📌 1️⃣  Get all users with posts:"
echo "GET $BASE_URL/users/"
curl -s -X GET "$BASE_URL/users/" \
  -H "Accept: application/json" | python -m json.tool

# 2. Get specific user
echo -e "\n\n📌 2️⃣  Get user with ID 1:"
echo "GET $BASE_URL/users/1/"
curl -s -X GET "$BASE_URL/users/1/" \
  -H "Accept: application/json" | python -m json.tool

# 3. Get user's posts (custom action)
echo -e "\n\n📌 3️⃣  Get posts for user 1:"
echo "GET $BASE_URL/users/1/posts/"
curl -s -X GET "$BASE_URL/users/1/posts/" \
  -H "Accept: application/json" | python -m json.tool

# 4. Get all posts
echo -e "\n\n📌 4️⃣  Get all posts:"
echo "GET $BASE_URL/posts/"
curl -s -X GET "$BASE_URL/posts/" \
  -H "Accept: application/json" | python -m json.tool

# 5. Get specific post
echo -e "\n\n📌 5️⃣  Get post with ID 1:"
echo "GET $BASE_URL/posts/1/"
curl -s -X GET "$BASE_URL/posts/1/" \
  -H "Accept: application/json" | python -m json.tool

# 6. Create new post (with auth)
echo -e "\n\n📌 6️⃣  Create new post:"
echo "POST $BASE_URL/posts/ (authenticated as $USER)"
curl -s -X POST "$BASE_URL/posts/" \
  -H "Content-Type: application/json" \
  -u "$USER:$PASS" \
  -d '{
    "title": "Новый товар от скрипта",
    "content": "Это пост создан через curl скрипт"
  }' | python -m json.tool

echo -e "\n\n✅ Test completed!"
echo "================================"
