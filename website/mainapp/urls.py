from django.conf.urls import url

from mainapp.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    ]
