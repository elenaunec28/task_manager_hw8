from django.shortcuts import render

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


ACCESS_COOKIE = 'access_token'
REFRESH_COOKIE = 'refresh_token'


def set_auth_cookies(response, access, refresh): #cookies, обновление токена
    response.set_cookie(
        key=ACCESS_COOKIE,
        value=str(access),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
    )
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=str(refresh),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
    )
    return response


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response(
                {'detail': 'Неверный логин или пароль.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({
            'user': {'id': user.id, 'username': user.username, 'email': user.email},
            'access': str(access),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
        return set_auth_cookies(response, access, refresh)


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE) or request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh-токен не найден.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {'detail': 'Refresh-токен недействителен или аннулирован.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access = serializer.validated_data['access']
        new_refresh = serializer.validated_data.get('refresh', refresh_token)

        response = Response({'detail': 'Токен обновлён.', 'access': access})
        return set_auth_cookies(response, access, new_refresh)


class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE) or request.data.get('refresh')

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass

        response = Response({'detail': 'Вы вышли из аккаунта.'}, status=status.HTTP_200_OK)
        response.delete_cookie(ACCESS_COOKIE)
        response.delete_cookie(REFRESH_COOKIE)
        return response