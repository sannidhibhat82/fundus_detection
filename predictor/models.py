from django.db import models

# Create your models here.
class UploadedModel(models.Model):
    model_file = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_file.name