from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

import os, glob
from detect import detectfaces, detectfeatures

import decimal

uploaded_file_url = ''
current_image = 'pic01.jpg'

def get_images_list(directory):
    files = glob.glob(directory + '/*.jpg')
    files.sort(key=os.path.getmtime)
    images_list = [ os.path.basename(x) for x in files[::-1] ]
    return images_list

class IndexView(TemplateView):

    template_name = 'index.html'
    title = "It's not our FAULT!"

    casc_dict = {'fault': False, 'trap': False, 'face': False, 'bottle': False}
    pars_dict = {'neighbors': 3, 'scale': 1.2, 'min': 20, 'max': 80}
    uploaded_file_url = ''
    current_image = 'pic01.jpg'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title

        for key, value in self.casc_dict.iteritems():
            context[key] = value
        for key, value in self.pars_dict.iteritems():
            context[key] = value
        context['images_loc'] = FileSystemStorage().location
        context['images_list'] = get_images_list(context['images_loc'])
        context['current_image'] = current_image
        print 'GET ' + current_image
        print 'GET ' + uploaded_file_url
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
            context['images_loc'] = fs.location
            context['images_list'] = get_images_list(context['images_loc'])

        global uploaded_file_url
        global current_image
        context['uploaded_file_url'] = uploaded_file_url

        cascades = ['fault', 'trap', 'face', 'bottle']
        for c in cascades:
            if request.POST.get(c):
                self.casc_dict[c] = True
            else:
                self.casc_dict[c] = False

        if 'neighbors' in request.POST:
            self.pars_dict['neighbors'] = int(request.POST['neighbors'])
        if 'scale' in request.POST:
            self.pars_dict['scale'] = float(request.POST['scale'])
        if 'min' in request.POST:
            self.pars_dict['min'] = int(request.POST['min'])
        if 'max' in request.POST:
            self.pars_dict['max'] = int(request.POST['max'])

        if uploaded_file_url:
            print(self.casc_dict)
            result_file_url = detectfeatures(context['uploaded_file_url'], self.casc_dict, scale_fact=self.pars_dict['scale'],
                    nbrs=self.pars_dict['neighbors'], minsize=self.pars_dict['min'], maxsize=self.pars_dict['max'])
            context['result_file_url'] = result_file_url
            current_image = os.path.basename(result_file_url)
            context['current_image'] = current_image
	
        print context['current_image']

        for key, value in self.casc_dict.iteritems():
            context[key] = value
        for key, value in self.pars_dict.iteritems():
            context[key] = value

        print request.POST
        print 'POST ' + current_image
        print 'POST ' + uploaded_file_url
        return super(TemplateView, self).render_to_response(context)
