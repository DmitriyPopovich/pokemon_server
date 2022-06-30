from django.urls import re_path
from .views import (
    LoginAPIView,
    RegistrationAPIView,
)
app_name = 'auth'


urlpatterns = [
    re_path(r'^login/?$', LoginAPIView.as_view(), name='login'),
    re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='registration'),
]
