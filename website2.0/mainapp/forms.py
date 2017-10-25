from django import forms
from mainapp.models import ImageDetections

class UploadForm(forms.ModelForm):
    class Meta:
        model = ImageDetections
        fields = ('picture',)

class SelectFeaturesForm(forms.ModelForm):
    class Meta:
        model = ImageDetections
        fields = ('face','bottle','fault','trap',)

class ImageDetectionForm(forms.ModelForm):
    class Meta:
        model = ImageDetections
        fields = ['picture','face','bottle','fault','trap','neighbors','scale','minsize','maxsize']

