# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 16:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HCG', '0008_auto_20170515_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='dishFavourited',
        ),
    ]
