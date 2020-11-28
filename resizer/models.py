from django.db import models

from django.urls import reverse
# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to="original_image", verbose_name="Не измененное изображение")
    resized_image = models.ImageField(upload_to="resized_image", verbose_name="Измененное изображение", null=True, blank=True)

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return reverse("resizer:detail", args=[self.pk])