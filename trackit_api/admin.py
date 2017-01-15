from django.contrib import admin
from trackit_api.models import *
from django.db.models import get_models,get_app

# Registering the models
for model in get_models(get_app('trackit_api')):
	admin.site.register(model)