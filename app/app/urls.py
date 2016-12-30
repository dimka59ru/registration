from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<status>[0-9]+)/$', views.filter_status, name='filter_status'),
    url(r'^edit/(?P<project_id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^add/$', views.add, name='add'),
    url(r'^search/$', views.search, name='search'),
    url(r'^report/$', views.report, name='report'),




    # url(r'^add/$', views.AddView.as_view(), name='add'),
    # url(r'^get_name/$', views.get_name, name='get_name'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

