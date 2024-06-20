from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField() #user w

    class Meta:
        model = User
        fields = ['id', 'username', 'password'] 


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'bio', 'profile_picture']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M') #Python's strftime function.
    
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'created_at', 'image']

class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = ['id', 'title', 'image', 'created_at']