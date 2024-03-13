
from django.urls import path, include
from.views import *


urlpatterns = [
    path('chatbot/', chatbot, name='chatbot'),
    path('generate/', generate_ppt, name='generate'),
 
]