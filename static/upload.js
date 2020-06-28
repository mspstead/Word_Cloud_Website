$('#upload-image').click(function() {
    event.preventDefault();
    var form_data = new FormData($('#upload-form')[0]);
    $('#upload-image').html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Uploading...').addClass('disabled');
    $.ajax({
        type: 'POST',
        url: '/upload',
        data: form_data,
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
        $('#upload-image').html('Upload').addClass('enabled');
        if(data['name'] == 'That file type is not supported.'){
            alert('That file type is not supported.');
        }
        else if(data['name'] == 'File size too large'){
            alert('File size too large');
        }
        else if(data['name'] == 'No file selected'){
            alert('No file selected');
        }
        else {
            my_url = "{{ url_for('upload', filename="+data['path']+" }}";
            $("#uploadImage").attr('src', data['path']); // setting the src attribute of img tag
            $('#upload-modal').modal('toggle');
        };
    }).fail(function(data){
        $('#upload-image').html('Upload').addClass('enabled');
        alert('error!');
    });
});