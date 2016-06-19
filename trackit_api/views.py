from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError,ParseError
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from tasks import add_product
from trackit_api.models import *
from trackit_api.serializers import UserSerializer
from rest_framework import status
# from LinkedinAuth import LinkedinOauthClient
import re


class Index(APIView):
	def get(self,request):
		return render(request,'trackit_api/index.html')
	def post(self,request):
		pass
class Validationfailed(ParseError):
	default_detail = "Please provide valid produt url"

class AddProduct(APIView):
	"""
		To add products
	"""
	def validate_url(self,url):
		"""
			validation of the requested 'url'
		"""
		product_asin = re.findall("([A-Z0-9]{10})",url)
		if not product_asin:
			raise Validationfailed()
		else:
			return True

	def get(self,request):
		"""
			add product to db using celery task
		"""
		url = request.GET['url']
		if self.validate_url(url):
			#call celery task
			#checking whether the user is authenticated or not
			if request.session.get('username'):
				user=request.session['username']
				add_product.delay(url,user)
			#if not authenticated add product with anonymous user
			else:
				print "anonymous user"
				user = 'anonymous'
				add_product.delay(url,user)


def listings(user):
	subscribed_products = Subscription.objects.filter(user=user)
	product_list=[]
	for product in subscribed_products:
		data={}
		price = product.product.product_price
		data["id"] = product.product.product_id
		data["name"] = product.product.product_name
		data["availability"] = product.product.product_availability
		data["extra_data"] = product.product.product_extra_data
		data["image"] = product.product.product_image
		product_list.append(data)
	response_data = {'product_list':product_list}
	try:
		return response_data
	except:
		raise DataUnavailable()
	
class Authenticate(APIView):
	def post(self,request):
		username = request.data['username']
		password = request.data['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				#return all subscribed products :-)

				subscribed_data = listings(user)
				request.session["username"] = user.username
				return Response(subscribed_data)
				print "session created"
			else:
				print 'inactive user'
	def delete(self,request):
		logout(request)
		print "logout success"
		content = {'user logout succesfully!!'}
		# return Response(content,status=status.HTTP_200_OK)
	
	# def get(self,request):
	# 	user= 'rijesh'
	# 	subscribed_data = listings(user)
	# 	print subscribed_data
	# 	return render(request,'trackit_api/index.html',{"name":user,"subscribed_data":subscribed_data})

#signup code here
class Signup(APIView):
	def post(self,request):
		#process the input
		serialized = UserSerializer(data=request.DATA)
		if serialized.is_valid():
			data_to_db = User.objects.create_user(
            serialized.validated_data['email'],
            serialized.validated_data['username'],
            serialized.validated_data['password']
        	)
        	if not data_to_db==None:
        		print "user added to db succesfully",data_to_db.username
        		request.session['user_name'] = data_to_db.username
        		subscribed_data = listings(user)
        	return Response(subscribed_data)


class Fetchall(APIView):
	def get(self,request):
		if request.session.get('username'):
			user = request.session['username']
			subscribed_data = listings(user)
			return Response(subscribed_data)
		return Response({'No data Available'})
		# return render(request,'trackit_api/index.html',{"name":user,"subscribed_data":subscribed_data})