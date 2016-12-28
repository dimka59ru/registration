# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('realization', 'partner', 'end_customer', 'email', 'contacts', 'file', 'note')
        labels = {
            'realization': _('Срок реализации'),
            'partner': _('Контрагент'),
            'end_customer': _('Конечный заказчик'),
            'contacts': _('Контакты'),
            'file': _('Файл'),
            'note': _('Прмечание'),
        }




