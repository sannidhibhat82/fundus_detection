import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ImageUploadForm
from predictor.models import UploadedModel
from gradio_client import Client, handle_file

# Initialize Gradio Client
GRADIO_CLIENT = Client("sannidhi82/fundus-detection")

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            img_path = os.path.join(settings.MEDIA_ROOT, uploaded_image.name)
            
            # Save the uploaded image
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            with open(img_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            try:
                # Send image to the Gradio API for prediction
                img_url = handle_file(img_path)
                result = GRADIO_CLIENT.predict(img=img_url, api_name="/predict")

                # Print debug information
                print('API response:', result)

            except Exception as e:
                print(f"Error during API call: {e}")
                result = {'error': str(e)}

            # Create the URL for the uploaded image
            image_url = os.path.join(settings.MEDIA_URL, uploaded_image.name)

            # Return the prediction result to the template
            return render(request, 'result.html', {'predicted_label': result, 'image_path': image_url})
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
