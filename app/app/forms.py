# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput
from .models import Project, Devices
from django import forms
from django.forms.formsets import BaseFormSet


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


class DeviceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        devices = Devices.objects.order_by('device_name')
        self.fields['device'] = forms.ChoiceField(
            choices=((x.device_name, x.device_name) for x in devices))

    sum = forms.IntegerField()


class AddDeviceForm(ModelForm):
    class Meta:
        model = Devices
        fields = ('device_name',)
        labels = {'device_name': _('Название')}


class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        devices = []
        sums = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                device = form.cleaned_data['device']
                sum = form.cleaned_data['sum']

                # Check that no two links have the same anchor or URL
                if device and sum:
                    # if deivce in deivces:1
                    #     duplicates = True
                    devices.append(device)

                    # if sum in sums:
                    #     duplicates = True
                    sums.append(sum)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if sum and not device:
                    raise forms.ValidationError(
                        'All links must have an anchor.',
                        code='missing_anchor'
                    )
                elif device and not sum:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_URL'
                    )
