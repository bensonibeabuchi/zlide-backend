from django.db import models
from users.models import CustomUser
import uuid

# Create your models here.


class Blog(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(max_length=255, blank=True, default="images/default_image.jpg", upload_to="images/")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(max_length=1000, unique=True, )
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
