from rest_framework import serializers
from profiles.models import Profile, ProfileStatus
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "last_login", "email", "date_joined"]


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    photo = serializers.ImageField(read_only=True)
    user = UserSerializer(read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_user_name(self, data):
        return f"{data.user.username}"


class ProfilePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["photo"]


class ProfileStatusSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"


class LoginDtoSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        print(data, "objesi burada")

        # Kullanıcı adı ve şifre boş olmamalı
        if not username:
            raise serializers.ValidationError("Kullanıcı adı gereklidir.")
        if not password:
            raise serializers.ValidationError("Şifre gereklidir.")

        for field_name in data.keys():
            if field_name not in ["username", "password"]:
                raise serializers.ValidationError(
                    f"{field_name} alanı beklenmedik bir alan."
                )

        return data
