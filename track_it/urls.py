"""track_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from trackit_api import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^Home/',views.Index.as_view()),
    url(r'^product/',views.AddProduct.as_view()),
    url(r'^authenticate/',views.Authenticate.as_view()),
    url(r'^fetchall/',views.Fetchall.as_view()),
    url(r'^signup/',views.Signup.as_view()),
    url(r'^subscription/user=(?P<user>(\w+))/',views.Getsubscription.as_view()),
    url(r'^history/id=(?P<id>([0-9A-Z]{,10}))/',views.PriceHistory.as_view()),
    url(r'^resetpassword/',views.Resetpassword.as_view()),
    url(r'^/verify/(?P<key>(.*))/email=(?P<email>(.*))',views.verify.as_view()),
    url(r'^account/applyresetpassword/',views.Applyresetpassword.as_view()),
    url(r'^notify',views.Notify.as_view())

]
