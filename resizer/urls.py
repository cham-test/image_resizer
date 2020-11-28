from django.urls import path

from .views import ImagesListView, ImageDetailView, UploadImageView, ResizeImageVIew

app_name = "resizer"

urlpatterns = [
    path('list/', ImagesListView.as_view(), name="list"),
    path('detail/<int:pk>', ImageDetailView.as_view(), name="detail"),
    path('upload/', UploadImageView.as_view(), name="upload"),
    path('resize/', ResizeImageVIew.as_view(), name='resize')
]