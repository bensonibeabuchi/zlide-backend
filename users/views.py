from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from djoser.social.views import ProviderAuthView
from .serializers import UserCreateSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


class CustomProviderAuthView(ProviderAuthView):
    @extend_schema(
        operation_id='Google/Facebook Authentication',
        description='This endpoint is used to Login with Google/Facebook',
        summary='This endpoint is used to Login with Google/Facebook',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)

            if response.status_code == 201:
                access_token = response.data.get('access')
                refresh_token = response.data.get('refresh')

                response.set_cookie(
                    'access',
                    access_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )
                response.set_cookie(
                    'refresh',
                    refresh_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )

            return response


class CustomTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        operation_id='Login with JWT Token',
        description='This endpoint is used to Login with with JWT Token',
        summary='This endpoint is used to Login with JWT Token. The Token is stored using http cookies automatically',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
      @extend_schema(
        operation_id='Refresh JWT Token',
        description='This endpoint refreshes the JWT Token',
        summary='This endpoint is used to refresh the JWT Token. The Token is then stored using http cookies automatically',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )
      
      def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    @extend_schema(
        operation_id='Verify JWT Token',
        description='This endpoint verifies the JWT Token',
        summary='This endpoint is used to verify the JWT Token. The Token is then stored using http cookies automatically',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    @extend_schema(
        operation_id='Logout Endpoint',
        description='This endpoint logs out the user by deleting the cookie from the browser.',
        summary='This endpoint logs out the user by deleting the cookie from the browser.',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )
    
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response

def index(request):
    return render(request, 'users/index.html')

