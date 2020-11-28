import requests

from PIL import Image as PilImage

from django.shortcuts import get_object_or_404, render

from django.urls import reverse

from django.core.files.base import ContentFile

from django.views.generic import ListView, FormView

from django.core.exceptions import ObjectDoesNotExist

from .models import Image, ResizedImage
from .forms import SizeForm, UploadForm
# Create your views here.


class ImageMixin:
    def get_image_name(self, path: str = None) -> str:
        if not path:
            image = get_object_or_404(Image, pk=self.kwargs["pk"])
            path = image.image.name
        return path[path.rfind('/') + 1:]

    def resize_image(self, width, height):
        image: Image = get_object_or_404(Image, pk=self.kwargs["pk"])
        image_content: ContentFile = ContentFile(image.image.read())
        resized_image: ResizedImage = ResizedImage.objects.update_or_create(original_image=image)[0]
        resized_image.resized_image.save(name=self.get_image_name(),
                                         content=image_content)

        pil_image = PilImage.open(resized_image.resized_image.path)
        pil_image = pil_image.resize((width, height))
        pil_image.save(resized_image.resized_image.path)
        return resized_image

    def get_context_sizes(self) -> dict:
        image: Image = get_object_or_404(Image, pk=self.kwargs["pk"])
        try:
            return {
                "width": image.resizedimage.resized_image.width,
                "height": image.resizedimage.resized_image.height
            }

        except ObjectDoesNotExist:
            return {
                "width": image.image.width,
                "height": image.image.height
            }

    def save_image_from_url(self, url: str) -> Image:
        binary_content: bytes = requests.get(url).content
        image_content: ContentFile = ContentFile(binary_content)
        image = Image.objects.create()
        image.image.save(name=self.get_image_name(url),
                         content=image_content)
        return image


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


class UploadImageView(FormView, ImageMixin):
    template_name = "resizer/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        if form.cleaned_data["url"] and form.cleaned_data["image"]:
            error: str = "Нужно ввести только одно поле"
            return render(self.request, self.template_name, {"error": error})

        if form.cleaned_data["url"]:
            image: Image = self.save_image_from_url(form.cleaned_data["url"])
            self.success_url = reverse("resizer:detail", args=[image.pk])
            return super().form_valid(form)

        print(form.files)
        if form.cleaned_data["image"]:
            image = Image()
            image.image = form.cleaned_data["image"]
            image.save()
            print("here")
            self.success_url = reverse("resizer:detail", args=[image.pk])
            return super().form_valid(form)



