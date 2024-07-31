# views.py
import os
import numpy as np
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from tensorflow.keras import models
from tensorflow.keras.preprocessing import image
from predictor.models import UploadedModel
from django.shortcuts import render, redirect


def get_vgg_modal():
    # Load the trained model
    try:
        modal_instance = UploadedModel.objects.last()
        if modal_instance: 
            print(modal_instance) 
            vgg_modal = models.load_model(modal_instance.model_file.path)
        else:
            vgg_modal = models.load_model(os.path.join(settings.BASE_DIR, 'static', 'models', 'mymodal.h5'))
        return vgg_modal
    except Exception as e:
        return None

# Function to load and preprocess the image
def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# View for handling image upload
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            img_name = uploaded_image.name
            img_path = os.path.join(settings.MEDIA_ROOT, img_name)
            
            # Save the uploaded image
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            with open(img_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            # Make prediction
            img_array = load_and_preprocess_image(img_path)
            predictions = get_vgg_modal().predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)[0]

            # Define the label map
            label_map = {0: 'Glaucoma', 1: 'Cataract', 2: 'Diabetic Retinopathy', 3: 'Normal'}

            # Check if predicted_class is valid
            if predicted_class in label_map:
                predicted_label = label_map[predicted_class]
            else:
                predicted_label = "Unknown disease detected. Please consult a specialist."


            # Create the URL for the uploaded image
            image_url = os.path.join(settings.MEDIA_URL, img_name)

            # Return the prediction result to the template
            return render(request, 'result.html', {'predicted_label': predicted_label, 'image_path': image_url})

        else:
            print(form.errors)

    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})



def upload_model(request):
    if request.method == 'POST':
        uploaded_model = request.FILES['model']
        
        # Save the model file to the database
        uploaded_instance = UploadedModel(model_file=uploaded_model)
        uploaded_instance.save()
        
        return redirect('predict_disease')  # Redirect to the disease prediction page

    return render(request, 'upload_model.html')