# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_devices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='note',
            field=models.CharField(max_length=300),
        ),
    ]
