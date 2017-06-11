from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

import os, glob
from detect import detectfaces, detectfeatures

def get_images_list(directory):
    files = glob.glob(directory + '/*.jpg')
    files.sort(key=os.path.getmtime)
    images_list = [ os.path.basename(x) for x in files[::-1] ]
    return images_list

class IndexView(TemplateView):

    template_name = 'index.html'
    title = "It's not our FAULT!"

    casc_dict = {'fault': False, 'trap': False, 'face': False, 'bottle': False}
    uploaded_file_url = ''

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title

        for key, value in self.casc_dict.iteritems():
            context[key] = value
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
            self.uploaded_file_url = fs.url(filename)
            context['uploaded_file_url'] = self.uploaded_file_url
            context['images_loc'] = fs.location
            context['images_list'] = get_images_list(context['images_loc'])

        cascades = ['fault', 'trap', 'face', 'bottle']
        for c in cascades:
            if request.POST.get(c):
                self.casc_dict[c] = True
            else:
                self.casc_dict[c] = False

        if self.uploaded_file_url:
            result_file_url = detectfeatures(self.uploaded_file_url, self.casc_dict)
            context['result_file_url'] = result_file_url
	

        for key, value in self.casc_dict.iteritems():
            context[key] = value

        print request.POST
        return super(TemplateView, self).render_to_response(context)
