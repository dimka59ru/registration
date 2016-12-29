# -*- coding: utf-8 -*-
from datetime import date
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

# from project_registration_django import settings
from django.conf import settings
from .models import Project, Devices, ListDevices, get_date_end
from .forms import ProjectForm

NOT_ACTUAL = 1  # Неактуальный
IMPLEMENTED = 2  # Реализованный
ACTUAL = 3  # Актуальный
OUTDATED = 4  # Устаревший


def count_project():
    project_list = Project.objects.all()
    stat = {'all': len(project_list), 'actual': len(project_list.filter(status=ACTUAL)),
            'implemented': len(project_list.filter(status=IMPLEMENTED)),
            'outdated': len(project_list.filter(status=OUTDATED)),
            'notactual': len(project_list.filter(status=NOT_ACTUAL))}
    return stat


def index(request):
    project_list = Project.objects.order_by('-status', '-id')
    device_list = ListDevices.objects.order_by('device_name')

    for project in project_list:

        if (date.today() > project.end_date) and (project.status == ACTUAL):
            project.status = OUTDATED
            project.save()
            messages.add_message(request, settings.MY_SUPER_ERROR, 'Проект {} истек '.format(project.id))

    context = {'project_list': project_list, 'device_list': device_list, 'stat': count_project()}
    return render(request, 'app/index.html', context)


def filter_status(request, status):
    project_list = Project.objects.order_by('-id').filter(status=status)
    device_list = ListDevices.objects.order_by('device_name')
    context = {'project_list': project_list, 'device_list': device_list, 'stat': count_project()}
    return render(request, 'app/index.html', context)


def add(request):
    flag_error = False
    device_list = Devices.objects.order_by('device_name')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST, request.FILES)

        devices_list_from_form = request.POST.getlist('checkbox')
        if not devices_list_from_form:
            messages.add_message(request, settings.MY_SUPER_ERROR, 'Не выбрано оборудование!')
            flag_error = True
        else:
            for device in devices_list_from_form:
                if not request.POST.get('{}_sum'.format(device)):
                    messages.add_message(request, settings.MY_SUPER_ERROR,
                                         'Не указано количество оборудования {}.'.format(device))
                    flag_error = True

        # check whether it's valid:
        if form.is_valid() and not flag_error:
            new_project = form.save()

            for device in devices_list_from_form:
                entry = ListDevices(device_name=device, sum=request.POST.get('{}_sum'.format(device)),
                                    id_project=new_project)
                entry.save()

            messages.add_message(request, settings.MY_SUPER_ERROR, 'Успешно добавлен!')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'app/add.html', {'form': form, 'device_list': device_list})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'app/add.html', {'form': form, 'device_list': device_list})


def edit(request, project_id):
    try:
        project = Project.objects.get(id=project_id)

        if request.method == 'POST' and request.POST['email']:
            project.email = request.POST['email']
            project.contacts = request.POST['contacts']
            project.note = request.POST['note']
            if request.POST['status']:
                project.status = request.POST['status']

            if request.POST['status'] == '1':
                messages.add_message(request, settings.MY_SUPER_ERROR, 'Больше не актуальный!  :(')
            elif request.POST['status'] == '2':
                messages.add_message(request, settings.MY_SUPER_ERROR, 'Ура! Реализован! :)')
            elif request.POST['status'] == '3':
                messages.add_message(request, settings.MY_SUPER_ERROR, 'Снова актуальный!  :)')
            elif request.POST['status'] == '4':
                project.status = ACTUAL
                project.end_date = get_date_end()
                messages.add_message(request, settings.MY_SUPER_ERROR, 'Продлен!  :)')

            else:
                messages.add_message(request, settings.MY_SUPER_ERROR, 'Успешно!')

            project.save()
            return HttpResponseRedirect('/')

        return render(request, 'app/edit.html', {'project': project})

    except Project.DoesNotExist:
        messages.add_message(request, settings.MY_SUPER_ERROR, 'Проект не найден!')

    return render(request, 'app/edit.html')


def search(request):
    dev = ''
    partner = ''
    consumer = ''
    gt = None
    lt = None

    project_list = Project.objects.order_by('-status', '-id')
    device_list = ListDevices.objects.order_by('device_name')

    if 'dev' in request.GET and request.GET['dev']:
        dev = request.GET['dev']
        project_list = project_list.filter(
            listdevices__device_name__icontains=dev).annotate(Count("pk"))
    if ('gt' in request.GET and request.GET['gt']) and ('lt' in request.GET and not request.GET['lt']):
        gt = request.GET['gt']
        project_list = project_list.filter(
            listdevices__sum__gte=int(gt)).annotate(Count("pk"))

    elif ('lt' in request.GET and request.GET['lt']) and ('gt' in request.GET and not request.GET['gt']):
        lt = request.GET['lt']
        project_list = project_list.filter(
            listdevices__sum__lte=int(lt)).annotate(Count("pk"))

    elif 'lt' in request.GET and request.GET['lt'] and 'gt' in request.GET and request.GET['gt']:
        lt = request.GET['lt']
        gt = request.GET['gt']
        project_list = project_list.filter(
            listdevices__sum__lte=int(lt),
            listdevices__sum__gte=int(gt)).annotate(Count("pk"))

    if 'partner' in request.GET and request.GET['partner']:
        partner = request.GET['partner']
        project_list = project_list.filter(partner__icontains=partner)

    if 'consumer' in request.GET and request.GET['consumer']:
        consumer = request.GET['consumer']
        project_list = project_list.filter(end_customer__icontains=consumer)

    context = {'project_list': project_list, 'device_list': device_list, 'stat': count_project(),
               'dev': dev, 'partner': partner, 'consumer': consumer, 'gt': gt, 'lt': lt}
    return render(request, 'app/index.html', context)


def report(request):
    device_list = Devices.objects.order_by('device_name').values()

    actual_projects = count_device(ACTUAL, device_list)
    not_actual_projects = count_device(NOT_ACTUAL, device_list)
    implemented_projects = count_device(IMPLEMENTED, device_list)
    outdated_projects = count_device(OUTDATED, device_list)
    all_projects = count_device(0, device_list)

    context = {'device_list': device_list, 'actual_projects': actual_projects,
               'not_actual_projects': not_actual_projects, 'implemented_projects': implemented_projects,
               'outdated_projects': outdated_projects, 'all_projects': all_projects}
    return render(request, 'app/report.html', context)


def count_device(status, device_list):
    result = {}

    if status != 0:
        projects = Project.objects.filter(status=status).values_list('pk', flat=True)
    else:
        projects = Project.objects.all().values_list('pk', flat=True)

    list_device_and_project = ListDevices.objects.filter(id_project__in=list(projects)).values()

    for device in device_list:
        sum = 0
        for device_and_project in list_device_and_project:
            if device['device_name'] == device_and_project['device_name']:
                sum += device_and_project['sum']
        result[device['device_name']] = sum

    return result
