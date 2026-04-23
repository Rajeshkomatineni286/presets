from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

from .models import UploadedImage
from .presets import PRESETS


@csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage

def upload_image(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Only POST allowed'}, status=405)

        file = request.FILES.get('image')

        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # Save file safely
        file_path = default_storage.save(f'uploads/{file.name}', file)

        return JsonResponse({
            'message': 'Upload successful',
            'file_path': file_path
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def apply_preset(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    image_id = request.POST.get('image_id')
    preset_name = request.POST.get('preset')

    if not image_id or not preset_name:
        return JsonResponse({'error': 'image_id and preset are required'}, status=400)

    if preset_name not in PRESETS:
        return JsonResponse({'error': f'Unsupported preset: {preset_name}'}, status=400)

    try:
        uploaded = UploadedImage.objects.get(pk=image_id)
    except UploadedImage.DoesNotExist:
        return JsonResponse({'error': 'Image not found'}, status=404)

    with Image.open(uploaded.original.path) as image:
        processed = PRESETS[preset_name](image.convert('RGB'))
        buffer = BytesIO()
        processed.save(buffer, format='JPEG', quality=92)
        buffer.seek(0)

        output_name = f"{Path(uploaded.original.name).stem}_{preset_name}.jpg"
        uploaded.processed.save(output_name, ContentFile(buffer.read()), save=True)

    return JsonResponse({
        'id': uploaded.id,
        'preset': preset_name,
        'processed_url': request.build_absolute_uri(uploaded.processed.url),
    })
