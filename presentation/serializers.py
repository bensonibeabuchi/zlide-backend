from rest_framework import serializers
from .models import *

class ZlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zlide
        fields = ['id', 'presentation_name', 'created_at', 'presentation_data',  ]