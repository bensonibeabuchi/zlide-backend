from django.shortcuts import render
import openai, os
from django.http import JsonResponse
from pptx import Presentation
from pptx.util import Pt
from dotenv import load_dotenv
import json
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.generics import RetrieveUpdateDestroyAPIView



load_dotenv()
api_key = os.getenv("OPENAI_KEY")


def get_chatbot_response(user_input):
    openai.api_key = api_key
    # user_input = request.POST.get('user_input')
    prompt = f"write a 3 slide content for a powerpoint presentation with slides, titles and content and convert them into a Json array with each item having a slide, title, content about: {user_input}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        temperature=0.5
    )
    chatbot_response = response.choices[0].message.content
    
    if response.choices:
        return json.loads(response.choices[0].message.content)
    else:
        return chatbot_response
    

def generate_slides(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        chatbot_response = get_chatbot_response(user_input)
        
        if chatbot_response:
            # Save the presentation data to the database or perform other operations
            presentation_data = Zlide.objects.create(data=chatbot_response)
            
            return JsonResponse({'message': 'Presentation created successfully', 'presentation_data': presentation_data})
        else:
            return JsonResponse({'error': 'Failed to get chatbot response'})
    else:
        return render(request, 'users/generate.html')

class GenerateSlidesAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ZlideSerializer
    
   
    @extend_schema(
        operation_id='Create Slides',
        description='This endpoint takes in user_input and gives out a json file containing the slide information',
        summary='This endpoint takes in user_input and gives out a json file containing the slide information',
        request= OpenApiTypes.OBJECT,
        responses={200: ZlideSerializer},
        parameters=[
            OpenApiParameter(
                name='user_input',
                description='User input for generating slides',
                required= True,
                type = OpenApiTypes.STR,
                
            )
        ]
    )
    def post(self, request):
        user_input = request.data.get('user_input')
        chatbot_response = get_chatbot_response(user_input)

        if chatbot_response:
            # Create a new Zlide object and save the presentation data
            zlide_serializer = ZlideSerializer(data={'presentation_data': chatbot_response})
            if zlide_serializer.is_valid():
                zlide_serializer.save()
                return Response({'message': 'Presentation created successfully', 'presentation_data': chatbot_response})
            else:
                return Response(zlide_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Failed to get chatbot response'}, status=status.HTTP_400_BAD_REQUEST)

    
    @extend_schema(
        operation_id='List Slides',
        description='This endpoint gets ALL the slides from the database for now',
        summary='This endpoint gets ALL the slides from the database for now',
        request= OpenApiTypes.OBJECT,
        responses={200: ZlideSerializer},
    )   
    def get(self, request):
        serialized_zlide = Zlide.objects.all()
        serialized_zlide = ZlideSerializer(serialized_zlide, many=True)
        return Response(serialized_zlide.data, status=status.HTTP_200_OK)



class ZlideDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Zlide.objects.all()
    serializer_class = ZlideSerializer


    @extend_schema(
        operation_id='Retrieve a Zlide object by its ID',
        description='Retrieve a Zlide object by its ID',
        summary='Retrieve a Zlide object by its ID',
        responses={200: ZlideSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=ZlideSerializer,
        operation_id='Update a Zlide object',
        description='Update a Zlide object by its ID.',
        summary='Update a Zlide object by its ID.',
        responses={200: ZlideSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @extend_schema(
        request=ZlideSerializer,
        operation_id='Update an entire Zlide object',
        description='Update an entire Zlide object by its ID.',
        summary='Update an entire Zlide object by its ID.',
        responses={200: ZlideSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id='Delete a Zlide object',
        description='Delete a Zlide object by its ID.',
        summary='Delete a Zlide object by its ID.',
        responses={204: ZlideSerializer},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)