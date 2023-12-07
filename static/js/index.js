document.querySelector('.custom-image-input').addEventListener('change', function (e) {
    
    if (e.target.files.length > 0) {
        var fileName = e.target.files[0].name;
    var maxLength = 20; // maximum number of characters to extract

    // truncate file name (preferably in the middle)
    var truncated = fileName;
    if (fileName.length > maxLength) {
        // truncate string in the middle
        truncated = fileName.substr(0, maxLength / 2) + '...' + fileName.substr(fileName.length - maxLength / 2, fileName.length);
    }

    // truncated text content as custom file label
    var fileLabel = document.querySelector('.custom-image-label');
    fileLabel.textContent = truncated;
    };
});