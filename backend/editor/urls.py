from django.urls import path

from .views import apply_preset, upload_image


def test_upload(request):
    return JsonResponse({"message": "upload route working"})


urlpatterns = [
    path('upload/', upload_image),
    path('apply-preset/', apply_preset),
]
