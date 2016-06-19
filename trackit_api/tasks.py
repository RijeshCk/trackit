from celery import shared_task
from trackit_api.models import *
from parsers import amazonparser
import re
import datetime
# from scripts import send_email_notification
import requests

@shared_task
def add_product(url,user):
	raw_asin = re.findall("([A-Z0-9]{10})",url)
	if raw_asin:
		asin = raw_asin[0]
	else:
		asin = re.findall("([A-Z0-9]{10})",url)[0]
	try:
		data_from_db = ProductData.objects.get(product_id=asin)
		
		try:
			#checking whether the user is already subscribed the product
			#do nothing in such cases
			Subscription.objects.get(user = user,product=data_from_db)	
		
		except Subscription.DoesNotExist:
			
			Subscription(user = user,product=data_from_db).save()
		
		except:
			pass
			
	except ProductData.DoesNotExist:
		
		print 'Adding New product to db'
		data = amazonparser.parse(url)
		price = data['price']
		availability = data['availability']
		product_id = data['product_id']
		DatafromSite = ProductData(product_price = price,product_previous_price=price,product_name = data["name"],product_availability = availability,product_url = url,product_id=product_id,product_image=data["image"])
		DatafromSite.save()
		PriceData = PriceDetails(price=price,product=DatafromSite,date=datetime.datetime.now())
		PriceData.save()
		Subscription(user = user,product=DatafromSite).save()
		return data
	
	except:
		#product already in database
		pass

@shared_task
def refresh():
	send_email_notification('Product Refresh started')
	products_to_refresh = ProductData.objects.all()

	for product in products_to_refresh:
		data = parser.parse(product.product_url)
		price = data['price']
		product_availability = data['availability']
		PriceData = PriceDetails(price = price, product = product, date = datetime.datetime.now())
		PriceData.save()
		product.product_availability = product_availability
		product.product_previous_price  = product.product_price
		product.product_price = price
		try:
			product.save()
		except:
			pass
		print "[updating ]:",product.product_id
	send_email_notification('Product Refresh Completed')

@shared_task
def keep_alive_task():
	#To keep the site alive
	response = requests.get("https://pricetrack-api.herokuapp.com/index")