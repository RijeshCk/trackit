# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(max_length=20)),
                ('access_token', models.CharField(max_length=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PriceDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=400, blank=True)),
                ('product_price', models.FloatField()),
                ('product_url', models.URLField(max_length=400)),
                ('product_id', models.CharField(unique=True, max_length=200)),
                ('product_previous_price', models.FloatField(default=0)),
                ('product_extra_data', jsonfield.fields.JSONField(default={})),
                ('product_availability', models.CharField(max_length=50)),
                ('product_image', models.CharField(max_length=500, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=50)),
                ('product', models.ForeignKey(to='trackit_api.ProductData')),
            ],
        ),
        migrations.AddField(
            model_name='pricedetails',
            name='product',
            field=models.ForeignKey(to='trackit_api.ProductData'),
        ),
    ]
