from rest_framework import generics
from profiles.models import Profile
from profiles.api.serializers import ProfileSerializer
import json
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from django.db.models import Q
from profiles.db.crud import CrudFunction
from profiles.auth.auth_service import ExampleAuthentication
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import check_password
import jwt
from profiles.api.serializers import UserSerializer
from profiles.api.serializers import LoginDtoSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from profiles.api.permission import IsOwnerProfileOrReadOnly
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProfileView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    crud_function = CrudFunction
    authentication_classes = [ExampleAuthentication]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["id", "user__username", "bio", "city"]
    # def get_queryset(self):
    #     return super().get_queryset()

    def list(self, request, *args, **kwargs):
        return self.crud_function.crud_list(self, request, *args, **kwargs)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    crud_function = CrudFunction
    permission_classes = [IsOwnerProfileOrReadOnly]
    authentication_classes = [ExampleAuthentication]


class AuthView(generics.GenericAPIView):

    def get_object(self, model, key, value):
        user_instance = get_object_or_404(model, **{key: value})
        return user_instance

    def post(self, request, *args, **kwargs):
        login_serializer = LoginDtoSerializer(data=request.data)
        if login_serializer.is_valid() == False:
            raise ValidationError({"data": login_serializer.errors}, code=400)

        user = self.get_object(
            model=User, key="username", value=request.data.get("username")
        )
        control_password = check_password(
            request.data.get("password"),
            user.password,
        )
        if control_password:
            payload = {
                "id": user.id,
                "username": user.username,
                "exp": datetime.utcnow()
                + timedelta(days=1),  # Token'ın 1 gün sonra süresi dolacak
            }
            profile = self.get_object(model=Profile, key="user", value=user)
            profile_serializer = ProfileSerializer(profile)
            encoded = jwt.encode(payload, "secret", algorithm="HS256")
            return Response(
                {"user": profile_serializer.data, "token": encoded}, status=200
            )
        else:
            raise ValidationError({"data": "Invalid password"}, code=401)


class ProfileViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [ExampleAuthentication]
