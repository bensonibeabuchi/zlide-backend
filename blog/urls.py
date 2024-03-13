
from django.urls import path, include
from .views import *


urlpatterns = [
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),

]