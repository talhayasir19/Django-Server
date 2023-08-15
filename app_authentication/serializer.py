
from rest_framework import serializers
from .models import AppUser
import uuid


class AppUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields =['email', 'first_name', 'last_name', 'is_staff', 'password']


    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user:AppUser = AppUser.objects.create(**validated_data)
        user.set_password(raw_password=password)
        user.save()
        return user


        

class LoginSeriliazer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()
    
    
        
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff','is_verified']

