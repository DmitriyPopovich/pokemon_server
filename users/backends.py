import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import AdvUser


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()

        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None
        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    @staticmethod
    def _authenticate_credentials(request, token):
        try:
            payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms='HS256')
        except Exception:
            msg = 'AuthenticationFailed Error'
            raise exceptions.AuthenticationFailed(msg)
        try:
            user = AdvUser.objects.get(pk=payload['id'])
        except AdvUser.DoesNotExist:
            msg = 'AuthenticationFailed Error user not found'
            raise exceptions.AuthenticationFailed(msg)
        if not user.is_active:
            msg = 'AuthenticationFailed Error User deactivated'
            raise exceptions.AuthenticationFailed(msg)
        return user, token
