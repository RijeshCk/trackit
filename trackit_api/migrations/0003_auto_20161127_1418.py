# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trackit_api', '0002_pricedropdetails_userdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricedropdetails',
            name='user',
            field=models.OneToOneField(to='trackit_api.UserDetails'),
        ),
    ]
