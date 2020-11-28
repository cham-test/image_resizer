from typing import Optional

from PIL import Image as PilImage

from django.shortcuts import get_object_or_404

from django.urls import reverse

from django.core.files.base import ContentFile

from django.views.generic import ListView, DetailView, FormView

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Image, ResizedImage
from .forms import SizeForm
# Create your views here.

class ImageMixin:
    @property
    def get_image_name(self) -> str:
        image = get_object_or_404(Image, pk=self.kwargs["pk"])
        path = image.image.name
        return path[path.rfind('/') + 1:]

    def resize_image(self, width, height):
        image: Image = get_object_or_404(Image, pk=self.kwargs["pk"])
        image_content: ContentFile = ContentFile(image.image.read())
        resized_image: ResizedImage = ResizedImage.objects.update_or_create(original_image=image)[0]
        resized_image.resized_image.save(name=self.get_image_name,
                                         content=image_content)

        pil_image = PilImage.open(resized_image.resized_image.path)
        pil_image = pil_image.resize((width, height))
        pil_image.save(resized_image.resized_image.path)
        return resized_image

    def get_context_sizes(self) -> dict:
        image: Image = get_object_or_404(Image, pk=self.kwargs["pk"])
        if image.resizedimage:
            return {
                "width": image.resizedimage.resized_image.width,
                "height": image.resizedimage.resized_image.height
            }
        else:
            return {
                "width": image.image.width,
                "height": image.image.height
            }

class ImagesListView(ListView):
    template_name = "resizer/list.html"
    context_object_name = "images"
    model = Image

class ImageDetailView(FormView, ImageMixin):
    template_name = "resizer/detail.html"
    form_class = SizeForm

    def form_valid(self, form):
        self.success_url = reverse("resizer:detail", args=[self.kwargs["pk"]])
        context_sizes = self.get_context_sizes()
        width: int = form.cleaned_data["width"] or context_sizes["width"]
        height: int = form.cleaned_data["height"] or context_sizes["height"]
        self.resize_image(width, height)
        return super(ImageDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image"] = get_object_or_404(Image, pk=self.kwargs["pk"])
        return context


class UploadImageView(FormView):
    pass

class ResizeImageVIew(FormView):
    pass