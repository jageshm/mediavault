document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file');
    const progressContainer = document.getElementById('upload-progress-container');
    const progressBar = document.getElementById('upload-progress');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Only intercept if there's a file selected
            if (fileInput.files.length > 0) {
                e.preventDefault();
                uploadFile();
            }
        });
    }
    
    // Handle file upload with progress tracking
    function uploadFile() {
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        // Create and configure the AJAX request
        const xhr = new XMLHttpRequest();
        
        // Setup progress event
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                const percentComplete = Math.round((e.loaded / e.total) * 100);
                
                // Update progress bar
                progressContainer.classList.remove('d-none');
                progressBar.style.width = percentComplete + '%';
                progressBar.setAttribute('aria-valuenow', percentComplete);
                progressBar.textContent = percentComplete + '%';
                
                // Change color based on progress
                if (percentComplete < 25) {
                    progressBar.classList.remove('bg-success', 'bg-info', 'bg-warning');
                } else if (percentComplete < 50) {
                    progressBar.classList.remove('bg-success', 'bg-warning');
                    progressBar.classList.add('bg-info');
                } else if (percentComplete < 75) {
                    progressBar.classList.remove('bg-success', 'bg-info');
                    progressBar.classList.add('bg-warning');
                } else {
                    progressBar.classList.remove('bg-info', 'bg-warning');
                    progressBar.classList.add('bg-success');
                }
            }
        });
        
        // Setup completion handler
        xhr.addEventListener('load', function() {
            if (xhr.status === 200) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    }
                } catch (e) {
                    // If not JSON, it's probably the full HTML page
                    window.location.href = '/gallery';
                }
            } else {
                alert('Upload failed. Please try again.');
                progressContainer.classList.add('d-none');
            }
        });
        
        // Setup error handler
        xhr.addEventListener('error', function() {
            alert('Upload failed. Please try again.');
            progressContainer.classList.add('d-none');
        });
        
        // Setup abort handler
        xhr.addEventListener('abort', function() {
            alert('Upload aborted.');
            progressContainer.classList.add('d-none');
        });
        
        // Send the request
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send(formData);
    }
});
