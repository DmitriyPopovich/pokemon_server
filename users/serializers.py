from rest_framework import serializers, exceptions
from users.models import AdvUser
from django.contrib.auth import authenticate


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = AdvUser
        fields = ('email', 'token', 'password')

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            msg = 'A email is required to log in.'
            raise exceptions.AuthenticationFailed(msg)
        if password is None:
            msg = 'A password is required to log in.'
            raise exceptions.AuthenticationFailed(msg)
        user = authenticate(username=email, password=password)
        if user is None:
            msg = 'A user with this email and password was not found'
            raise exceptions.AuthenticationFailed(msg)
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        access_token = user.token

        return {
            'email': user.email,
            'token': access_token,
        }


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = AdvUser
        fields = ('email', 'token', 'password', 'password2')

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        password2 = data.get('password2', None)

        if password and password2 and password != password2:
            msg = 'Check input passwords.'
            raise exceptions.AuthenticationFailed(msg)
        if email is None:
            msg = 'A email is required to log in.'
            raise exceptions.AuthenticationFailed(msg)
        if password is None:
            msg = 'A password is required to log in.'
            raise exceptions.AuthenticationFailed(msg)
        user = AdvUser.objects.filter(email=email)
        if user.count():
            msg = f'User with mail {email} already exists.'
            raise exceptions.AuthenticationFailed(msg)
        return data

    def create(self, validated_data):
        try:
            validated_data.pop('password2')

            user = AdvUser.objects.create_user(**validated_data)
        except Exception:
            msg = 'Error create user'
            raise exceptions.AuthenticationFailed(msg)
        return user

