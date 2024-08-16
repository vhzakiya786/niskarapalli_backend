from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from user_app.serializers import LoginSerializer
# Create your views here.


class Login(TokenObtainPairView):
    serializer_class=LoginSerializer