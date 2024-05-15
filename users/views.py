from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from djoser.social.views import ProviderAuthView
from .serializers import UserCreateSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny
from users.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from djoser.views import UserViewSet
from rest_framework.decorators import action
from django.conf import settings
from .serializers import *
from rest_framework import generics
import random
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags



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



def generate_otp():
    return str(random.randint(100000, 999999))


class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        otp = generate_otp()
        user.otp = otp  # Save the OTP to the user model or another model
        user.save()

        email = user.email
        current_site = get_current_site(self.request)
        subject = 'Please Activate your account'
        html_message = render_to_string('users/activation.html', {
            'user': user,
            'domain': current_site.domain,
            'otp': otp,
            'site_name': settings.SITE_NAME,
        })
        from_email = 'bensonibeabuchistudios@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = user.email
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()



class CustomActivationView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        operation_id='Activate user using OTP',
        description='This endpoint activates a user using OTP',
        summary='This endpoint is used to activate a user using the OTP sent to their email.',
        request= OpenApiTypes.OBJECT,
        responses={200: CustomUserSerializer},
        )
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not email or not otp:
            return Response({'error': _('Email and OTP are required.')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': _('User does not exist.')}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.otp == otp:
            user.is_active = True
            user.otp = None  # Clear the OTP after activation
            user.save()

            email = user.email
            current_site = get_current_site(self.request)
            subject = 'Account activated successufully'
            protocol = 'https' if self.request.is_secure() else 'http'
            html_message = render_to_string('users/confirmation.html', {
                'user': user,
                'domain': settings.DOMAIN,
                'protocol': protocol,
                'site_name': settings.SITE_NAME,
            })
            from_email = 'bensonibeabuchistudios@gmail.com'
            plain_message = strip_tags(html_message)
            to_email = user.email

            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return Response({'message': _('Account activated successfully.')}, status=status.HTTP_200_OK)
        else:
            return Response({'error': _('Invalid OTP.')}, status=status.HTTP_400_BAD_REQUEST)




class SendOTPView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        operation_id='Resend OTP to user',
        description='This endpoint resends OTP to user',
        summary='This endpoint is used to resend OTP to user provided they have their email address.',
        request= OpenApiTypes.OBJECT,
        responses={200: CustomUserSerializer},
        )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'error': _('Email is required.')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': _('User does not exist.')}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        user.otp = otp  # Save the OTP to the user model or another model
        user.save()

        email = user.email
        current_site = get_current_site(self.request)
        subject = 'Please Activate your account'
        html_message = render_to_string('users/resendotp.html', {
                'user': user,
                'domain': current_site.domain,
                'otp': otp,
                'site_name': settings.SITE_NAME,
            })
        from_email = 'bensonibeabuchistudios@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = user.email

        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()