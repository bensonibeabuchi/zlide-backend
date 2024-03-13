from django.db import models
from users.models import CustomUser
import uuid

# Create your models here.


class Testimonial(models.Model):

    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    review = models.TextField()
    author = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='author_testimonials')
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Testimonial by {self.author.email}"
