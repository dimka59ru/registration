# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20161216_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='file',
            field=models.FileField(upload_to='doc/'),
        ),
    ]
