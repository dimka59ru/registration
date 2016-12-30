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

    device_list = Devices.objects.order_by('device_name')
    deivce = forms.ChoiceField(choices=((x.device_name, x.device_name) for x in device_list))
    sum = forms.IntegerField()



class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        deivces = []
        sums = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                deivce = form.cleaned_data['deivce']
                sum = form.cleaned_data['sum']

                # Check that no two links have the same anchor or URL
                if deivce and sum:
                    # if deivce in deivces:
                    #     duplicates = True
                    deivces.append(deivce)

                    # if sum in sums:
                    #     duplicates = True
                    sums.append(sum)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if sum and not deivce:
                    raise forms.ValidationError(
                        'All links must have an anchor.',
                        code='missing_anchor'
                    )
                elif deivce and not sum:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_URL'
                    )
