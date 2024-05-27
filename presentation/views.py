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
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from openai import OpenAI
from decouple import config
import requests
from django.views import View
from rest_framework.generics import ListCreateAPIView





load_dotenv()
api_key = os.getenv("OPENAI_KEY")
UNSPLASH_ACCESS_KEY = config('UNSPLASH_ACCESS_KEY')

client = OpenAI()




# def get_unsplash_images(query, per_page=10):
#     url = f"https://api.unsplash.com/search/photos"
#     headers = {
#         "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
#     }
#     params = {
#         "query": query,    # The search query term
#         "per_page": per_page  # Number of results per page
#     }
    
#     response = requests.get(url, headers=headers, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
#         images = data['results']
#         image_urls = [image['urls']['regular'] for image in images]
#         return image_urls
#     else:
#         print(f"Error fetching images: {response.status_code}")
#         return []
    
def get_unsplash_images(query, per_page=10):
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,    # The search query term
        "per_page": per_page  # Number of results per page
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        images = data['results']
        
        # Hardcoded width and height
        width = 440
        height = 520
        
        # Generate the image URLs with hardcoded width and height parameters
        image_urls = []
        for image in images:
            image_url = image['urls']['regular']
            image_url += f'&w={width}&h={height}'
            image_urls.append(image_url)
        
        return image_urls
    else:
        print(f"Error fetching images: {response.status_code}")
        return []

    
def get_chatbot_response(user_input):
    openai.api_key = api_key
    prompt = f"following Guy kawasaki principles, generate a 10 page pitch deck with slides, titles and an explanatory robust content and convert them into a Json array with each item having a slide, title, content about: {user_input}. The title should only contain title text without naming what slide it is"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,  # Increase the maximum number of tokens
        temperature=0.7   # Set temperature for creativity
        )
    print(f'{response.usage.prompt_tokens} prompt tokens used.')
    chatbot_response = response.choices[0].message.content
    
    if response.choices:
        try:
            return json.loads(chatbot_response)
        except json.JSONDecodeError:
            # Handle JSON decoding error if the response is not a valid JSON
            return {"error": "Invalid JSON response"}
    else:
        return {"error": "No response from the model"}
    

# def openai_image_generation(user_input):
#     openai.api_key = api_key
#     prompt = {user_input}
#     response = client.images.generate(
#     model="dall-e-3",
#     prompt="a white siamese cat",
#     size="1024x1024",
#     quality="standard",
#     n=1,
#     )
#     print(f'{response.usage.prompt_tokens} prompt tokens used.')
#     image_url = response.data[0].url
    
#     if response.choices:
#         try:
#             return json.loads(image_url)
#         except json.JSONDecodeError:
#             # Handle JSON decoding error if the response is not a valid JSON
#             return {"error": "Invalid JSON response"}
#     else:
#         return {"error": "No response from the model"}
    

class GenerateSlidesAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ZlideSerializer

    @extend_schema(
        operation_id='Create Slides',
        description='This endpoint takes in user_input and gives out a json file containing the slide information',
        summary='This endpoint takes in user_input and gives out a json file containing the slide information',
        request=OpenApiTypes.OBJECT,
        responses={200: ZlideSerializer},
        parameters=[
            OpenApiParameter(
                name='user_input',
                description='User input for generating slides',
                required=True,
                type=OpenApiTypes.STR,
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        user_input = request.data.get('user_input')
        if not user_input:
            return Response({'error': 'user_input is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        slides_content = get_chatbot_response(user_input)
        
        if not slides_content:
            return Response({'error': 'Failed to generate slides content'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        combined_response = []

        for slide in slides_content:
            slide_content = slide.get('content', '')
            image_urls = get_unsplash_images(slide_content, per_page=1)
            slide['image_urls'] = image_urls
            combined_response.append(slide)

        zlide_data = {'presentation_data': combined_response,
                      'user': request.user.id  # Add the user ID to the zlide data
                      }
        zlide_serializer = self.get_serializer(data=zlide_data)
        
        if zlide_serializer.is_valid():
            zlide_serializer.save()
            return Response(zlide_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(zlide_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    @extend_schema(
        operation_id='List Slides',
        description='This endpoint gets ALL the slides from the database for now',
        summary='This endpoint gets ALL the slides from the database for now',
        request=OpenApiTypes.OBJECT,
        responses={200: ZlideSerializer},
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        user_zlides = Zlide.objects.filter(user=user) 
        # serialized_zlide = Zlide.objects.all()
        serialized_zlide = ZlideSerializer(user_zlides, many=True)
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
    

# class UnsplashImageView(View):
#     def get(self, request, *args, **kwargs):
#         user_input = request.GET.get('query', 'nature')  # Default to 'nature' if 'query' is not provided
#         slides_content = get_chatbot_response(user_input)
        
#         if not slides_content:
#             return JsonResponse({'error': 'Failed to generate slides content'}, status=500)

#         combined_response = []

#         for slide in slides_content:
#             slide_content = slide.get('content', '')
#             image_urls = get_unsplash_images(slide_content, per_page=1)
#             slide['image_urls'] = image_urls
#             combined_response.append(slide)
        
#         # return combined_response
#         return JsonResponse({'slides': combined_response}, status=200)





    

# def generate_slides(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')
#         chatbot_response = get_chatbot_response(user_input)
        
#         if chatbot_response:
#             # Save the presentation data to the database or perform other operations
#             presentation_data = Zlide.objects.create(data=chatbot_response)
            
#             return JsonResponse({'message': 'Presentation created successfully', 'presentation_data': presentation_data})
#         else:
#             return JsonResponse({'error': 'Failed to get chatbot response'})
#     else:
#         return render(request, 'users/generate.html')

# class GenerateSlidesAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = ZlideSerializer
    
   
#     @extend_schema(
#         operation_id='Create Slides',
#         description='This endpoint takes in user_input and gives out a json file containing the slide information',
#         summary='This endpoint takes in user_input and gives out a json file containing the slide information',
#         request= OpenApiTypes.OBJECT,
#         responses={200: ZlideSerializer},
#         parameters=[
#             OpenApiParameter(
#                 name='user_input',
#                 description='User input for generating slides',
#                 required= True,
#                 type = OpenApiTypes.STR,
                
#             )
#         ]
#     )
#     def post(self, request):
#         user_input = request.data.get('user_input')
#         chatbot_response = get_chatbot_response(user_input)
#         # chatbot_response = UnsplashImageView

#         if chatbot_response:
#             # Create a new Zlide object and save the presentation data
#             zlide_serializer = ZlideSerializer(data={'presentation_data': chatbot_response})
#             if zlide_serializer.is_valid():
#                 zlide_serializer.save()
#                 return Response({'message': 'Presentation created successfully', 'presentation_data': chatbot_response})
#             else:
#                 return Response(zlide_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'error': 'Failed to get chatbot response'}, status=status.HTTP_400_BAD_REQUEST)

    
#     @extend_schema(
#         operation_id='List Slides',
#         description='This endpoint gets ALL the slides from the database for now',
#         summary='This endpoint gets ALL the slides from the database for now',
#         request= OpenApiTypes.OBJECT,
#         responses={200: ZlideSerializer},
#     )   
#     def get(self, request):
#         serialized_zlide = Zlide.objects.all()
#         serialized_zlide = ZlideSerializer(serialized_zlide, many=True)
#         return Response(serialized_zlide.data, status=status.HTTP_200_OK)



