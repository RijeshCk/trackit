from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError,ParseError
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from tasks import *
from trackit_api.models import *
from trackit_api.serializers import UserSerializer,SubscriptionSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
# from LinkedinAuth import LinkedinOauthClient
import re,base64,datetime
from utils import send_confirmation
from track_it import settings
from config import *
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult


class Index(APIView):
	def get(self,request):
		return render(request,'trackit_api/index.html')
	def post(self,request):
		pass

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
		data['price'] = product.product.product_price
		product_list.append(data)
	response_data = {'product_list':product_list}
	try:
		return response_data
	except:
		raise DataUnavailable()

class Validationfailed(ParseError):
	default_detail = "Please provide valid product url"

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
				task = add_product.delay(url,user)
				while True:
					if task.status=='SUCCESS':
						user = request.session['username']
						subscribed_data = listings(user)
						return Response(subscribed_data)
					elif task.status=="FAILED":
						pass
					else:
						continue
				
				if task.status=='SUCCESS':
					print Fetchall.get(self,request)
				else:
					print Fetchall.get(self,request)

			#if not authenticated add product with anonymous user
			else:
				user = 'anonymous'
				task = add_product.delay(url,user)				
				if task.status=='SUCCESS':
					pass
	
class Authenticate(APIView):
	@csrf_exempt
	def post(self,request):

		username = request.data['username']
		password = request.data['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				subscribed_data = listings(user)
				request.session["username"] = user.username
				return Response(subscribed_data,status=status.HTTP_200_OK)
			else:
				subscribed_data = []
				return Response(subscribed_data,status.status.HTTP_404_NOT_FOUND)
	
	def delete(self,request):
		logout(request)
		content = {'user logout succesfully!!'}
		return Response(content,status=status.HTTP_200_OK)
	
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
				request.session['user_name'] = data_to_db.username
				subscribed_data = listings(user)
			return Response(subscribed_data)

def activationkey_generator(user):
	date = datetime.datetime.now()
	user = user
	unique_token_string = str(date)+user
	encoded_token_string = base64.b64encode(unique_token_string)
	return encoded_token_string

class Resetpassword(APIView):
	
	def post(self,request):
		email = request.data['email']
		if User.objects.filter(email=email).exists():
			User.objects.get(email=email)
			key = activationkey_generator(email)
			link = settings.BASE_URL+'/Home/#verify/'+key+'?email='+email
			redis_connection.set(key,key)
			redis_connection.expire(key,KEY_TIMEOUT)
			send_confirmation(email,link)

			return Response({'content':'An email with password reset instructions has been sent to '+email},status=status.HTTP_200_OK)
			#send reset link to mail
		else:
			content = {'content':' Entered email is not registered '}
			return Response(content, status=status.HTTP_404_NOT_FOUND)

class Applyresetpassword(APIView):
	
	def post(self,request):
		username = request.data['email']
		password = request.data['password']
		
		user = User.objects.get(username__exact = username)
		if user:
			user.set_password(password)
			user.save()
			content = {'content':' Password Updated Succesfully!! '}
			return Response(content,status = status.HTTP_204_NO_CONTENT)
		else:
			content = {'content': ' Failed to Update the Password '}
			return Response(content,status = status.HTTP_404_NOT_FOUND)

class verify(APIView):

	def get(self,request,key,email):
		if settings.redis_connection.exists(key):
			print "key exists"
			content = {'key_authenticated':True,'content':'','user':email}
			return Response(content,status = status.HTTP_200_OK)
		else:
			content = {'key_authenticated':False,'content':'','user':email}			
			print "key expired"
			return Response(content,status = status.HTTP_401_UNAUTHORIZED)
		#next step is to verify this key ,generate a form to reset the password
		
class Fetchall(APIView):
	def get(self,request):
		if request.session.get('username'):
			user = request.session['username']
			subscribed_data = listings(user)
			return Response(subscribed_data)
		return Response({'No data Available'})
		# return render(request,'trackit_api/index.html',{"name":user,"subscribed_data":subscribed_data})

class Getsubscription(APIView):
	serializer_class = SubscriptionSerializer
	def get(self,request,user):	
		subscribed_products=Subscription.objects.filter(user=user)
		all_subscribed_products = []
		for products in subscribed_products:
			subscribed_data = {
								'name':products.product.product_name,
								'price': products.product.product_price,
								'product_url': products.product.product_url,
								'product_id': products.product.product_id,
								'product_previous_price': products.product.product_previous_price,
								'product_availability': products.product.product_availability,
								'product_image': products.product.product_image,
			}
			all_subscribed_products.append(subscribed_data)
		return Response(all_subscribed_products)

class PriceHistory(APIView):
	def get(self,request,id):
		subscribed_products = PriceDetails.objects.filter(product__product_id=id)
		price_list = []
		for product in subscribed_products:
			data={
					"price":product.price,
					"date":product.date
				}
			price_list.append(data)
		return Response(price_list)

class Notify(APIView):
	def get(self,request):
		pass

	def post(self,request):
		product_id = request.data['product_id']
		drop_price = request.data['drop_price']
		# username = request.session["username"]
		username = "rijumon"
		try:
			product = ProductData.objects.get(product_id=product_id)
			
		except :
			context = {"error":"Product Does Not Exist"}
			return Response(context,status = status.HTTP_500_INTERNAL_SERVER_ERROR)
	
		try:
			result = PricedropDetails.objects.get(user=username,product=product)
			result.drop_value = drop_price
			result.save()
			RefreshUpdatedProduct.delay(product)
			#invoke the celery refresh task here
			context = {"updated"}
			return Response(context,status = status.HTTP_200_OK)
		except PricedropDetails.DoesNotExist:
			PricedropDetails(user=username,product=product,drop_value=drop_price).save()
			context = {"new product added"}
			return Response(context,status = status.HTTP_201_CREATED)
		except Exception as e:
			print "here",e