from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    picture = models.ImageField(upload_to = 'static/mainapp/uploads/')
