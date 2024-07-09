from django.utils.translation import gettext as _
from django.contrib.auth import password_validation, get_user_model

from rest_framework import exceptions, serializers, validators
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt import serializers as jwt_serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source="id", read_only=True)
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    email = serializers.EmailField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("userId", "firstName", "lastName", "email", "phone", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.organisations.create(name=f"{user.first_name.strip()}'s Organisation")
        return user


class CookieTokenObtainPairSerializer(jwt_serializers.TokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(write_only=True)
        self.fields["password"] = PasswordField(write_only=True)

    access = serializers.CharField(read_only=True, default=None)
    # refresh = serializers.CharField(read_only=True, default=None)

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except exceptions.AuthenticationFailed as e:
            raise exceptions.ValidationError(e.detail)
        return data
