from django.db import models

class ImageDetections(models.Model):
    picture = models.ImageField(upload_to = 'mainapp/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resultfile = models.ImageField(upload_to = 'mainapp/detected/',blank=True)
    face = models.BooleanField(default=False,blank=True)
    bottle = models.BooleanField(default=False,blank=True)
    fault = models.BooleanField(default=False,blank=True)
    trap = models.BooleanField(default=False,blank=True)
    neighbors = models.PositiveIntegerField(default=3)
    scale = models.DecimalField(default=1.2,max_digits=2, decimal_places=1)
    minsize = models.PositiveIntegerField(default=20)
    maxsize = models.PositiveIntegerField(default=80)
