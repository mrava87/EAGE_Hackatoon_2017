from django.conf.urls import url

from mainapp.views import IndexView, UploadView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<key>[a-zA-Z0-9]+)$', UploadView.as_view(), name='upload'),
    ]

