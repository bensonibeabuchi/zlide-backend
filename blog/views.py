from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from rest_framework import permissions



# Create your views here.

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the post
        return obj.author == request.user


class BlogView(APIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        operation_id='List all Blog post',
        description='This endpoint lists all single Blog post',
        summary='This endpoint lists all Blog post',
        responses={200: BlogSerializer},
    )
    def get(self, request):
        all_blog = Blog.objects.all()
        serialized_blogs = BlogSerializer(all_blog, many=True)
        return Response(serialized_blogs.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='Creates a single Blog post',
        description='This endpoint creates a single Blog and saves it to the database',
        summary='This endpoint creates a single Blog and saves it to the database',
        responses={200: BlogSerializer},
    )
    def post(self, request):
        # Associate the current user with the blog post
        request.data['author'] = request.user.id

        new_blog = BlogSerializer(data=request.data)
        new_blog.is_valid(raise_exception=True)
        new_blog.save()
        message = {"Success": "New Blog has been added successfully"}
        return Response(message, status=status.HTTP_201_CREATED)
    




class BlogDetailView(APIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @extend_schema(
        operation_id='Retrieves a single Blog object by its slug',
        description='This endpoint retrieves a single Blog from the database using slug as the unique identifier',
        summary='This endpoint retrieves a single Blog from the database using slug as the unique identifier',
        responses={200: BlogSerializer},
    )
    def get(self, request, slug):
        single_blog = Blog.objects.get(slug=slug)
        serialized_single = BlogSerializer(single_blog)
        return Response(serialized_single.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='Updates a single Blog object by its slug',
        description='This endpoint updates a single Blog from the database using slug as the unique identifier',
        summary='This endpoint updates a single Blog from the database using slug as the unique identifier',
        responses={200: BlogSerializer},
    )
    def put(self, request, slug):
        single_blog = Blog.objects.get(slug=slug)
        self.check_object_permissions(request, single_blog)  # Check if the user has permission
        update_blog = BlogSerializer(single_blog, data=request.data, partial=True)
        update_blog.is_valid(raise_exception=True)
        update_blog.save()
        message = {"Success" : "Blog updated Successfully"}
        return Response(message, status=status.HTTP_202_ACCEPTED)
    
    @extend_schema(
        operation_id='Delete a single Blog object by its slug',
        description='This endpoint deletes a single Blog from the database using slug as the unique identifier',
        summary='This endpoint deletes a single Blog from the database using slug as the unique identifier',
        responses={200: BlogSerializer},
    )
    def delete(self, request, slug):
        single_blog = Blog.objects.get(slug=slug)
        self.check_object_permissions(request, single_blog)  # Check if the user has permission
        single_blog.delete()
        message = {"Success" : "Blog has been deleted successfully"}
        return Response(message, status=status.HTTP_410_GONE)
