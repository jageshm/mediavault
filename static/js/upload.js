document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = uploadProgress.querySelector('.progress-bar');
    const fileInput = document.getElementById('file');
    
    // Check file size before upload
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const fileSize = this.files[0].size;
            // 16MB in bytes
            const maxSize = 16 * 1024 * 1024;
            
            if (fileSize > maxSize) {
                alert('File size exceeds 16MB limit. Please select a smaller file.');
                this.value = ''; // Clear the input
            }
        }
    });
    
    // Handle form submission with progress tracking
    uploadForm.addEventListener('submit', function(e) {
        // Only intercept if there's a file selected
        if (fileInput.files.length > 0) {
            e.preventDefault();
            
            // Create FormData object
            const formData = new FormData(uploadForm);
            
            // Create and configure XMLHttpRequest
            const xhr = new XMLHttpRequest();
            
            // Show progress bar and disable submit button
            uploadProgress.classList.remove('d-none');
            uploadBtn.disabled = true;
            uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Uploading...';
            
            // Track upload progress
            xhr.upload.addEventListener('progress', function(event) {
                if (event.lengthComputable) {
                    const percentComplete = Math.round((event.loaded / event.total) * 100);
                    progressBar.style.width = percentComplete + '%';
                    progressBar.setAttribute('aria-valuenow', percentComplete);
                    progressBar.textContent = percentComplete + '%';
                }
            });
            
            // Handle response
            xhr.addEventListener('load', function() {
                if (xhr.status === 200) {
                    // Redirect to the response URL (which should be the gallery page)
                    window.location = xhr.responseURL;
                } else {
                    // If we get an error response
                    alert('Upload failed. Please try again.');
                    
                    // Reset form state
                    uploadProgress.classList.add('d-none');
                    uploadBtn.disabled = false;
                    uploadBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Upload';
                }
            });
            
            // Handle network errors
            xhr.addEventListener('error', function() {
                alert('A network error occurred. Please try again.');
                
                // Reset form state
                uploadProgress.classList.add('d-none');
                uploadBtn.disabled = false;
                uploadBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Upload';
            });
            
            // Open and send the request
            xhr.open('POST', uploadForm.action, true);
            xhr.send(formData);
        }
    });
});
