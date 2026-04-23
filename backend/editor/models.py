from django.db import models


class UploadedImage(models.Model):
    original = models.ImageField(upload_to='originals/')
    processed = models.ImageField(upload_to='processed/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image {self.pk}'
