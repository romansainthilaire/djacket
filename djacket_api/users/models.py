from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator


class UserProfileManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(email=email, username=username, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-last_login"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(3)])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)

    must_change_password = models.BooleanField(default=False)
    temporary_password_sent_at = models.DateTimeField(null=True, blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
