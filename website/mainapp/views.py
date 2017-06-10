from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

import os, glob

def get_images_list(directory):
    files = glob.glob(directory + '/*.png')
    files.sort(key=os.path.getmtime)
    images_list = [ os.path.basename(x) for x in files[::-1] ]
    return images_list[:9]

class IndexView(TemplateView):

    template_name = 'index.html'
    title = "It's not our FAULT!"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title

        context['images_loc'] = FileSystemStorage().location
        context['images_list'] = get_images_list(context['images_loc'])
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if 'myfile' in request.FILES:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            fname_ext = myfile.name.split('.')
            ext = fname_ext[-1]
            fname = slugify('_'.join(fname_ext[:-1])) + '.' + ext
            filename = fs.save(fname, myfile)
            uploaded_file_url = fs.url(filename)
            context['uploaded_file_url'] = uploaded_file_url
            context['images_loc'] = fs.location
            context['images_list'] = get_images_list(context['images_loc'])

        return super(TemplateView, self).render_to_response(context)
