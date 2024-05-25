from django.db import models
from users.models import CustomUser

# Create your models here.

class Image(models.Model):
    phrase = models.CharField(max_length=512)
    ai_image = models.ImageField(upload_to='images/ai_image')

    def __str__(self):
        return str(self.phrase)

    
class Zlide(models.Model):
    presentation_name = models.CharField(max_length=256, default='Untitled Presentation', blank=True, null=True)
    presentation_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Zlide {self.id}"