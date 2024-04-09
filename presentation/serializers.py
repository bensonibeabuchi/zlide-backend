from rest_framework import serializers
from .models import *

class ZlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zlide
        fields = ['id', 'presentation_data', 'created_at']