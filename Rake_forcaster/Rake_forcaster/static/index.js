// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const submitButton = document.getElementById('submitButton');
    const cancelButton = document.getElementById('cancelButton');
    const errorMessage = document.getElementById('errorMessage');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    let selectedFile = null;

    uploadArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (event) => {
        event.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = event.dataTransfer.files;
        handleFiles(files);
    });

    uploadButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        const files = fileInput.files;
        handleFiles(files);
    });

    submitButton.addEventListener('click', () => {
        if (selectedFile) {
            uploadFile(selectedFile);
        }
    });

    cancelButton.addEventListener('click', () => {
        clearSelection();
    });

    function handleFiles(files) {
        errorMessage.textContent = '';
        fileList.innerHTML = '';
        selectedFile = null;
        submitButton.disabled = true;

        if (files.length > 0) {
            const file = files[0];
            if (file.type === "text/xml" || file.name.endsWith('.xml')) {
                const fileItem = document.createElement('p');
                fileItem.textContent = file.name;
                fileList.appendChild(fileItem);
                selectedFile = file;
                submitButton.disabled = false;
            } else {
                errorMessage.textContent = 'Please upload a valid XML file.';
            }
        }
    }

    function clearSelection() {
        fileInput.value = '';
        fileList.innerHTML = '';
        errorMessage.textContent = '';
        selectedFile = null;
        submitButton.disabled = true;
        progressContainer.hidden = true;
        progressBar.value = 0;
        progressText.textContent = '0%';
    }

    function uploadFile(file) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload'); // Django upload URL

        xhr.upload.addEventListener('progress', (event) => {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                progressBar.value = percentComplete;
                progressText.textContent = `${Math.round(percentComplete)}%`;
            }
        });

        xhr.addEventListener('load', () => {
            if (xhr.status == 200) {
                window.location.href = '/upload_success'; 
            } else {
                alert('File upload failed.');
            }
        });

        xhr.addEventListener('error', () => {
            alert('An error occurred during the file upload.');
        });

        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        progressContainer.hidden = false;
        const formData = new FormData();
        formData.append('file', file);
        xhr.send(formData);
    }
});
