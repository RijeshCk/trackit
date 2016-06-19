from django.contrib import admin
from trackit_api.models import *

# Register your models here.
@admin.register(ProductData)
class ProductDataAdmin(admin.ModelAdmin):
	pass
@admin.register(PriceDetails)
class PriceDetailsAdmin(admin.ModelAdmin):
	pass
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
	pass
@admin.register(CustomAuth)
class CustomAuthAdmin(admin.ModelAdmin):
	pass