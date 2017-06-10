import cv2
from django.shortcuts import render
from django.views.generic.base import View, TemplateView

class IndexView(TemplateView):

    template_name = 'index.html'
    title = "It's not our FAULT!"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['active'] = 'index'
        return context

