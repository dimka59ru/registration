import os
from datetime import date
from uuid import uuid4
from django.utils.deconstruct import deconstructible

from django.db import models




def get_date_end():
    new_year = date.today().year
    new_month = date.today().month + 3

    if new_month > 12:
        new_year += 1
        new_month -= 12

    return date(new_year, new_month, date.today().day)


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file        
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("doc/")


class Project(models.Model):
    status = models.IntegerField(default=3)
    add_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=get_date_end)
    realization = models.CharField(max_length=200)
    partner = models.CharField(max_length=300)
    end_customer = models.CharField(max_length=300)
    email = models.EmailField()
    contacts = models.TextField()
    file = models.FileField(upload_to=path_and_rename)
    note = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['status', 'id']

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super(Project, self).delete(*args, **kwargs)


class Devices(models.Model):
    device_name = models.CharField(max_length=300)


class ListDevices(models.Model):
    device_name = models.CharField(max_length=300)
    sum = models.IntegerField(default=0)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)





