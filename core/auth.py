# Router that handles user registration and login with token authentication
from ninja import Router
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from ninja.responses import Response
from django.db import IntegrityError


router = Router()

# Creates a new user and gives them a unique token
@router.post("/register")
def register(request, username: str, password: str):
    if not username or not password:
        return Response({"detail": "Username and password are required"}, status=400)
    if len(password) < 6:
        return Response({"detail": "Password must be at least 6 characters"}, status=400)

    try:
        user = User.objects.create_user(username=username, password=password)
    except IntegrityError:
        return Response({"detail": "Username already exists"}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=201)

# Logs in user and returns their token if credentials are correct
@router.post("/token")
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Invalid username or password"}, status=401)
    token, created = Token.objects.get_or_create(user=user) # Gets existing token or creates one if not exist
    return {"token": token.key}
