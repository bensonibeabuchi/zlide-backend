from djoser.serializers import UserCreateSerializer
from .models import *

class UserCreateSerializer(UserCreateSerializer):
    class Meta (UserCreateSerializer.Meta):
        model = CustomUser
        fields= ('id', 'email', 'password', 'first_name', 'last_name', 'job_title', 'company') 
