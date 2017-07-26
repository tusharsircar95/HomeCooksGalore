# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishName', models.CharField(max_length=250)),
                ('dishRating', models.IntegerField()),
                ('dishPublisher', models.CharField(max_length=250)),
                ('dishSteps', models.TextField(max_length=1000)),
            ],
        ),
    ]