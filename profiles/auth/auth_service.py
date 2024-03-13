import logging
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.validators import ValidationError
import jwt
from datetime import datetime, timedelta
from profiles.models import Profile


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")
        # development mode
        if authorization_header == None:
            authorization_header = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJpc21haWxha2NhYmV5IiwiZXhwIjoxNzEwNDE5NTc5fQ.a8UVEs_XXGibxI8whF8E_VSRi2ifWFUsVpwjXkZa8v4"
        # development mode
        if not authorization_header:
            raise ValidationError({"data": "Required auth token"}, code=401)
        parts = authorization_header.split()
        if parts[0].lower() != "bearer":
            # Eğer başlık "Bearer" ile başlamıyorsa hata fırlat
            raise exceptions.AuthenticationFailed("Bearer token is not found.")
        if len(parts) == 1:
            raise exceptions.AuthenticationFailed("Bearer token is not found.")
        elif len(parts) > 2:
            raise exceptions.AuthenticationFailed("Bearer token is not valid.")
        token = parts[1]
        algorithm = "HS256"
        secret_key = "secret"
        try:
            decoded_payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            try:
                user = User.objects.get(id=decoded_payload.get("id"))
                profile = Profile.objects.get(user=user.id)
                return (profile, None)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed({"data": "user not fount"})
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({"data": "JWT token expired."})
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed({"data": "invalid JWT token'ı."})
