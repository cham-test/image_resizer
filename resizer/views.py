from django.shortcuts import render

from django.views.generic import ListView, DetailView, FormView

from .models import Image
# Create your views here.

class ImagesListView(ListView):
    template_name = "resizer/list.html"
    context_object_name = "images"
    model = Image

class ImageDetailView(DetailView):
    pass

class UploadImageView(FormView):
    pass

class ResizeImageVIew(FormView):
    pass