from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *

from django.core.exceptions import ObjectDoesNotExist


class LogoutView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'users/index.html')


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'