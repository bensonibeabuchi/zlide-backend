from django.shortcuts import render
from rest_framework.generics import ListAPIView, DestroyAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView
from .models import Testimonial
from .serializers import TestimonialSerializer
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions



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
    


class TestimonialListCreate(APIView):
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    @extend_schema(
        operation_id='List Testimonials',
        description='This endpoint lists all the Testimonial in the database',
        summary='This endpoint lists all the Testimonial in the database',
        request= OpenApiTypes.OBJECT,
        responses={200: TestimonialSerializer},
    )
    def get(self, request):
        serialized_testimonial = Testimonial.objects.all()
        serialized_testimonial = TestimonialSerializer(serialized_testimonial, many=True)
        return Response(serialized_testimonial.data, status=status.HTTP_200_OK)
    

    @extend_schema(
        operation_id='Create Testimonials',
        description='This endpoint creates a new testimonial and saves it in the database',
        summary='This endpoint creates a new testimonial and saves it in the database',
        request= OpenApiTypes.OBJECT,
        responses={200: TestimonialSerializer},
        parameters=[
            OpenApiParameter(
                name='review',
                description='User Review',
                required= True,
                type = OpenApiTypes.STR,
                
            ),
            OpenApiParameter(
                name='rating',
                description='User Rating',
                required= True,
                type = OpenApiTypes.STR,
                
            )
        ]
    )
    def post(self, request):
        new_testimonial = TestimonialSerializer(data=request.data)
        # Associate the current user with the blog post
        request.data['author'] = request.user.id
        new_testimonial.is_valid(raise_exception=True)
        new_testimonial.save()
        message = {"Success": "New Testimonial has been added successfully"}
        return Response(message, status=status.HTTP_201_CREATED)




class TestimonialDetailView(APIView):
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @extend_schema(
        operation_id='Retrieve a single Testimonial object by its ID',
        description='This endpoint retrieves a single Testimonial from the database using id as the unique identifier',
        summary='This endpoint retrieves a single Testimonial from the database using id as the unique identifier',
        responses={200: TestimonialSerializer},
    )
    def get(self, request, id):
        single_testimonial = Testimonial.objects.get(id=id)
        serialized_single = TestimonialSerializer(single_testimonial)
        return Response(serialized_single.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='Update a single Testimonial object by its ID',
        description='This endpoint updates a single Testimonial from the database using id as the unique identifier',
        summary='This endpoint updates a single Testimonial from the database using id as the unique identifier',
        responses={200: TestimonialSerializer},
    )
    def put(self, request, id):
        single_testimonial = Testimonial.objects.get(id=id)
        self.check_object_permissions(request, single_testimonial)  # Check if the user has permission
        update_testimonial = TestimonialSerializer(single_testimonial, data=request.data, partial=True)
        update_testimonial.is_valid(raise_exception=True)
        update_testimonial.save()
        message = {"Success" : "Testimonial updated Successfully"}
        return Response(message, status=status.HTTP_202_ACCEPTED)
    
    @extend_schema(
        operation_id='Delete a single Testimonial object by its ID',
        description='This endpoint deletes a single Testimonial from the database using id as the unique identifier',
        summary='This endpoint deletes a single Testimonial from the database using id as the unique identifier',
        responses={200: TestimonialSerializer},
    )
    def delete(self, request, id):
        single_testimonial = Testimonial.objects.get(id=id)
        self.check_object_permissions(request, single_testimonial)  # Check if the user has permission
        single_testimonial.delete()
        message = {"Success" : "Testimonial has been deleted successfully"}
        return Response(message, status=status.HTTP_410_GONE)




