from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from PIL import Image

from .models import UploadedImage


class EditorApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def _build_image_upload(self, name='sample.png', color=(255, 0, 0)):
        buffer = BytesIO()
        image = Image.new('RGB', (32, 32), color=color)
        image.save(buffer, format='PNG')
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type='image/png')

    def test_upload_image_success(self):
        response = self.client.post('/api/upload/', {'image': self._build_image_upload()})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('id', payload)
        self.assertIn('original_url', payload)
        self.assertEqual(UploadedImage.objects.count(), 1)

    def test_upload_image_missing_file(self):
        response = self.client.post('/api/upload/', {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'No image provided')

    def test_apply_preset_success(self):
        upload_response = self.client.post('/api/upload/', {'image': self._build_image_upload()})
        image_id = upload_response.json()['id']

        response = self.client.post('/api/apply-preset/', {'image_id': image_id, 'preset': 'vintage'})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['preset'], 'vintage')

        uploaded = UploadedImage.objects.get(pk=image_id)
        self.assertTrue(bool(uploaded.processed))

    def test_apply_preset_invalid_name(self):
        upload_response = self.client.post('/api/upload/', {'image': self._build_image_upload()})
        image_id = upload_response.json()['id']

        response = self.client.post('/api/apply-preset/', {'image_id': image_id, 'preset': 'unknown'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Unsupported preset: unknown')
