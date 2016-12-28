import os
from datetime import date
from uuid import uuid4

from django.db import models




def get_date_end():
    new_year = date.today().year
    new_month = date.today().month + 3

    if new_month > 12:
        new_year += 1
        new_month -= 12

    return date(new_year, new_month, date.today().day)


def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

class Project(models.Model):
    status = models.IntegerField(default=3)
    add_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=get_date_end)
    realization = models.CharField(max_length=200)
    partner = models.CharField(max_length=300)
    end_customer = models.CharField(max_length=300)
    email = models.EmailField()
    contacts = models.TextField()
    file = models.FileField(upload_to=path_and_rename('doc/'))
    note = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['status', 'id']


class Devices(models.Model):
    device_name = models.CharField(max_length=300)


class ListDevices(models.Model):
    device_name = models.CharField(max_length=300)
    sum = models.IntegerField(default=0)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)





