from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ['name', 'age']  #All fields which we declare in models
        # exclude = ['id'] #All fields of models exclude "id"
        fields = '__all__'  #It includes all field of models

    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError({'error':'age cannot be less than 18'})
        
        if any(char.isdigit() for char in data['name']):
            raise serializers.ValidationError({'error': 'Name cannot contain digits'})
        
        return data
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']



class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Book
        fields = '__all__'
        #depth = 1      

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']