from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=UserProfile.objects.all(),
                message="Cette adresse e-mail est déjà utilisée."
            )
        ]
    )

    username = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(15),
            UniqueValidator(
                queryset=UserProfile.objects.all(),
                message="Ce nom d'utilisateur est déjà pris."
            ),
            RegexValidator(
                regex=r"^(?!.*_{2})[A-Za-z0-9](?:[A-Za-z0-9_]*[A-Za-z0-9])$",
                message=(
                    'Caractères autorisés : lettres, chiffres et "_". '
                    'Ne peut pas commencer ou finir par "_", ni contenir deux "_" consécutifs.'
                )
            )
        ]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "email",
            "username",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "created_at",
            "updated_at"
        ]

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return UserProfile.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("password", None)  # password updates should be done via ChangePasswordSerializer
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    def validate_new_password(self, value):
        try:
            validate_password(value, user=self.context.get("user"))
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError("New password must be different from old password.")
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            raise serializers.ValidationError({"invalid_credentials": "Invalid username or password."})

        user: UserProfile = self.user
        if not user.email_verified:
            raise serializers.ValidationError({"email_verified": "Email not verified."})
        return data
