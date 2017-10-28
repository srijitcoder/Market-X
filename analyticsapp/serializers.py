from rest_framework import serializers
from eventapp.models import *




class RetailerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Retailer
		fields = '__all__'
		


class ProductSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Product
		fields = '__all__'
		


class Product1Serializer(serializers.ModelSerializer):
	
	class Meta:
		model = Product
		fields = '__all__'
		

class Product2Serializer(serializers.ModelSerializer):
	
	class Meta:
		model = Product
		fields = '__all__'
		