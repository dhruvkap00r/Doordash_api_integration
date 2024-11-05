from rest_framework import serializers
from .models import *

#dropoff information is user info
class DasherInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Dasher
    fields = ['dasher_id', 'name', 'pickup_phone_number', 'dropoff_phone_number',       'vehicle_make', 'vehicle model', 'vehicle_year']

class DeliveryInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = DeliveryInfo
    fields = '__all__' 
  
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
  def create(self, validated_data):
        # Override to handle password hashing
    user = User(**validated_data)
    user.set_password(validated_data['password'])  # Hash the password
    user.save()
    return user

class RestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Restaurant_info
    fields = '__all__'