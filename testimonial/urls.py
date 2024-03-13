
from django.urls import path, include
from .views import *


urlpatterns = [
    path('testimonial/', TestimonialListCreate.as_view(), name='testimonial'),
    path('testimonial/<int:id>/', TestimonialDetailView.as_view(), name='testimonial-create'),

]