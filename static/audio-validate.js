function fileValidation(){
    var fileInput = document.getElementById('file');
    var filePath = fileInput.value;
    var allowedExtensions = /(\.ogg|\.wav|\.flac)$/i;
    if(!allowedExtensions.exec(filePath)){
        alert('Please upload file having extensions .ogg/.wav/.flac only.');
        fileInput.value = '';
        return false;
    }else{
        //Image preview
        if (fileInput.files && fileInput.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('validator').innerHTML = '<img src="check.png"/>';
            };
            reader.readAsDataURL(fileInput.files[0]);
        }
    }
}