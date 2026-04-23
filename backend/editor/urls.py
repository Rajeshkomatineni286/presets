from django.urls import path

from .views import apply_preset, upload_image

urlpatterns = [
    path('upload/', upload_image, name='upload-image'),
    path('apply-preset/', apply_preset, name='apply-preset'),
]
