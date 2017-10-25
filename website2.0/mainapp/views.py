from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.conf import settings

import os
from .detect import detectfeatures, detectfeatures2
from .models import ImageDetections
from .forms import ImageDetectionForm
from .utils import key_to_id, id_to_key

def get_image_list():
    imagelist = ImageDetections.objects.values_list('resultfile', flat=True)
    return [settings.MEDIA_URL + x for x in imagelist if x]

class IndexView(TemplateView):

    template_name = 'index.html'
    title = "It's not our FAULT!"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['images_list'] = get_image_list()
        context['model'] = ImageDetections()#ImageDetections.objects.get(id=1)
        return context

    def post(self, request, *args, **kwargs):

        if 'picture' in request.FILES:

            form = ImageDetectionForm(request.POST,request.FILES)
            model = form.save()
            detectfeatures2(model)
            url = 'upload-%s' % (id_to_key(model.id, os.environ.get('KEYSPACE','')))

            return HttpResponseRedirect(url)

        else:

            context = self.get_context_data()

            return super(TemplateView, self).render_to_response(context)

class UploadView(TemplateView):

    template_name = 'index.html'
    title = "It's not our FAULT!"

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['images_list'] = get_image_list()
        context['model'] = ImageDetections.objects.get(id=key_to_id(self.kwargs['key'],os.environ.get('KEYSPACE','')))
        return context

    def post(self, request, *args, **kwargs):

        if 'picture' in request.FILES:

            form = ImageDetectionForm(request.POST,request.FILES)
            model = form.save()
            detectfeatures2(model)
            url = 'upload-%s' % (id_to_key(model.id,os.environ.get('KEYSPACE','')))

            return HttpResponseRedirect(url)

        else:

            modelinstance = ImageDetections.objects.get(id=key_to_id(self.kwargs['key'],os.environ.get('KEYSPACE','')))
            form = ImageDetectionForm(request.POST, instance=modelinstance)
            form.save()
            form.instance.resultfile.delete()
            detectfeatures2(form.instance)

            context = self.get_context_data()

            return super(TemplateView, self).render_to_response(context)


