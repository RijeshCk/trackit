from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from trackit_api import models
from django.contrib.auth.models import User
from validate_email import  validate_email

class ProductSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	product_name = serializers.CharField(required =True, allow_blank=False, max_length=400)
	product_price = serializers.FloatField(required =True)
	product_url = serializers.CharField(required =True, allow_blank=False, max_length=400)
	product_id = serializers.CharField(required =True, allow_blank=False, max_length=10)
	product_previous_price = serializers.FloatField(required =True,)
	product_extra_data = serializers.CharField(max_length=400)
	product_availability = serializers.CharField(max_length=400)
	product_image = serializers.CharField(max_length=400)

	def create(self,validated_data):
		"""
			create and return a new 'Product'
		"""
		return ProductData.objects.create(**validated_data)
	class Meta:
		fields = ('product_name','product_price','product_url','product_id','product_previous_price','product_extra_data','product_availability','product_image')
	# def get_queryset(self):
	# 	print "inside get_queryset"
		

class UserSerializer(serializers.Serializer):

	username = serializers.CharField(required=True,allow_blank=False,max_length=50)
	email = serializers.EmailField(required=True,allow_blank=False,max_length=50)
	password = serializers.CharField(required=True,allow_blank=False,max_length=20)

	class Meta:
		model = 'user'
		fields = ('username','email','password')
	def validate(self,data):
		print data
		if not validate_email(data['email']):
			return serializers.ValidationError('Incorrect email')
		elif len(data['username'])<3:
			return serializers.ValidationError('name must contain atleast 3 letters')
		elif len(data['password'])<=5:
			return serializers.ValidationError('password length should be atleast 5')
		else :
			return data
			
	# def create(self, validated_data):
	# 	user = User.objects.create_user(
	# 		email = validated_data['email'],
	# 		username = validated_data['username'],
	# 		password = validated_data['password'],
	# 	)
	# 	return user
	# def create(self,va):
	# def validate_email(self,value):
		# if not "rij" in value:
			# raise serializers.ValidationError('name not starts with rij')
		# return value
class SubscriptionSerializer(serializers.ModelSerializer):
	user = serializers.CharField(required=True,allow_blank=False,max_length=50)
	product=serializers.StringRelatedField(many=True)
	class Meta:
		model = models.Subscription
		fields = ('user','product')