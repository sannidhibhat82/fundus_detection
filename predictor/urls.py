# predictor/urls.py
from django.urls import path
from .views import upload_image, upload_model


urlpatterns = [
    path('', upload_image, name='predict_disease'),
    path('upload_model/', upload_model, name='upload_model'),
]
