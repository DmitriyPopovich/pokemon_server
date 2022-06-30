from django.db import models
from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

import jwt
from datetime import datetime
from datetime import timedelta
from Pokemons import settings


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email name is necessary')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AdvUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(hours=settings.TIME_HOUR_LIVE_TOKEN_AUTHENTICATION)
        secret = settings.JWT_ACCESS_SECRET_KEY
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, secret, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'