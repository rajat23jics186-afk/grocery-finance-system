/* Upload functionality */

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

if (dropZone) {
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        handleFiles(files);
    });
}

if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

function handleFiles(files) {
    const formData = new FormData();
    for (let file of files) {
        formData.append('file', file);
    }

    const xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            console.log(`Upload progress: ${percentComplete}%`);
        }
    });

    xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
            console.log('Upload successful');
        }
    });

    xhr.open('POST', '/api/upload');
    xhr.send(formData);
}
