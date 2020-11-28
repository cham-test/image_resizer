from django.db import models

from django.urls import reverse
# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to="original_image", verbose_name="Не измененное изображение")

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return reverse("resizer:detail", args=[self.pk])

class ResizedImage(models.Model):
    original_image = models.OneToOneField(Image, models.CASCADE)
    resized_image = models.ImageField(upload_to="resized_image", verbose_name="Измененное изображение", null=True, blank=True)

    class Meta:
        verbose_name = "Измененная картинка"
        verbose_name_plural = "Измененные картинки"

    def __str__(self):
        return self.resized_image.name
