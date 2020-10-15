from rest_framework import serializers

from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        Model=User
        fields=['username','password']