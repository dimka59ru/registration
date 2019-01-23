import calendar
import os
from datetime import date
from uuid import uuid4
from django.utils.deconstruct import deconstructible

from django.db import models


def get_date_end():
    # возвращает новую дату. + 3 месяца к дате создания проекта. дата окончания проекта.
    #  new_date = datetime.date.today() + datetime.timedelta(days=91)  # рабочий вариант, не удалять
    #  return datetime.date(new_date.year, new_date.month, new_date.day)

    today = date.today()
    month = today.month - 1 + 3  # прибавляем 3 месяца
    year = int(today.year + month / 12)
    month = month % 12 + 1
    day = min(today.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


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
    # note = models.CharField(max_length=300, blank=True)
    note = models.TextField(max_length=3000, blank=True)

    class Meta:
        ordering = ['status', 'id']

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super(Project, self).delete(*args, **kwargs)

    # def __repr__(self):
    #     return str(self)


class Devices(models.Model):
    device_name = models.CharField(max_length=300)


class ListDevices(models.Model):
    device_name = models.CharField(max_length=300)
    sum = models.IntegerField(default=0)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __repr__(self):
        return "name: {}, id_project: {}, sum: {}\n".format(self.device_name, self.id_project.id, self.sum)
