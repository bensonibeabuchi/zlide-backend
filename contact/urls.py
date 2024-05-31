from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('contact/', ContactMessageView.as_view(), name='contact-view'),

]