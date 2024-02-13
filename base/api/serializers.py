from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Blog


class RegisterSerializer(serializers.Serializer): 
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username  = data['username']).exists():
            raise serializers.ValidationError('username is taken')
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(first_name = validated_data['first_name'],last_name = validated_data['last_name'],username= validated_data['username'].lower())
        user.set_password(validated_data['password'])
        user.save()
        

        return validated_data
    
    
class BlogSerializer(ModelSerializer):
    class Meta:
        model  = Blog
        exclude = ['created_at','updated_at']