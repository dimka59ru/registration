# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20161216_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
