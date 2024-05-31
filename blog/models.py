from django.db import models
from users.models import CustomUser
import uuid

# Create your models here.


class Blog(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(max_length=255, blank=True, default="images/default_image.jpg", upload_to="images/")
    image2 = models.ImageField(max_length=255, blank=True, null=True, default="images/default_image.jpg", upload_to="images/")
    image3 = models.ImageField(max_length=255, blank=True, null=True, default="images/default_image.jpg", upload_to="images/")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    writer = models.CharField(max_length=256, blank=True, null=True, default='Admin')
    slug = models.SlugField(max_length=1000, unique=True, )
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title
    
