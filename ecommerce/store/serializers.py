from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','phonenumber']

class OtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10)
    class Meta:
        fields = ['otp']
    
class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=100)
    class Meta:
        fields = ['search']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ["address",'city','state','zipcode']

