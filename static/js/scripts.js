document.addEventListener('DOMContentLoaded', function () {
    const uploadContainer = document.getElementById('uploadContainer');
    const imageUpload = document.getElementById('imageUpload');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const imagePreview = document.getElementById('imagePreview');
    const previewImage = document.getElementById('previewImage');
    const imageName = document.getElementById('imageName');
    const removeImage = document.getElementById('removeImage');

    // Check if elements exist before adding event listeners
    if (uploadContainer && imageUpload && submitBtn && imagePreview && previewImage && imageName && removeImage) {
        // Open the file dialog when the upload container is clicked
        uploadContainer.addEventListener('click', function () {
            if (submitBtn.disabled) {
                imageUpload.click();
            }
        });

        imageUpload.addEventListener('change', function () {
            const file = imageUpload.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                    imageName.textContent = file.name;
                    imagePreview.style.display = 'flex';
                    submitBtn.disabled = false; // Enable the button
                };
                reader.readAsDataURL(file);
            }
        });

        removeImage.addEventListener('click', function () {
            imageUpload.value = ''; // Clear the input
            imagePreview.style.display = 'none'; // Hide the preview
            submitBtn.disabled = true; // Disable the button
        });
    }
});
