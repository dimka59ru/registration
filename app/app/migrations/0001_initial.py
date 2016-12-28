# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 05:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=3)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(default=datetime.date(2015, 1, 1))),
                ('realization', models.CharField(max_length=200)),
                ('partner', models.CharField(max_length=300)),
                ('end_customer', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('contacts', models.TextField()),
                ('file', models.CharField(max_length=200)),
                ('note', models.TextField()),
            ],
        ),
    ]
