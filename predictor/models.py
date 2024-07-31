from django.db import models
import os
# Create your models here.
class UploadedModel(models.Model):
    model_file = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_file.name
    
def upload_path(instance, filename):
    return os.path.join('images', str(instance.pk), filename)
class ProjectImage(models.Model):
    images = models.FileField(null=True, blank=True,upload_to=upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.images.name