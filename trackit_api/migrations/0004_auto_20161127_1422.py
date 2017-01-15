# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trackit_api', '0003_auto_20161127_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricedropdetails',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
