$('#generateCloud').click(function() {
    event.preventDefault();
    console.log('Clicked')
    var silloutte_path = $('#uploadImage').attr('src');
    $.ajax({
        type: 'POST',
        url: '/process',
        data: silloutte_path,
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
          my_url = "{{ url_for('upload', filename="+data['cloud_file_path']+" }}";
          $("#cloud_image").attr('src', data['cloud_file_path']); // setting the src attribute of img tag
    }).fail(function(data){
        alert('error!');
    });
});