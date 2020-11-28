from django.contrib import admin

from .models import Image, ResizedImage
# Register your models here.

admin.site.register(Image)
admin.site.register(ResizedImage)
