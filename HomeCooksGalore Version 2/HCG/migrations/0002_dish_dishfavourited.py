# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCG', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='dishFavourited',
            field=models.BooleanField(default=False),
        ),
    ]
