from django.contrib import admin

# Register your models here.
from .models import ImageDetections

class ImageDetectionAdmin(admin.ModelAdmin):
    date_hierarchy = 'uploaded_at'
    list_display = ('picture','uploaded_at','id','face','bottle','fault','trap')


admin.site.register(ImageDetections, ImageDetectionAdmin)

