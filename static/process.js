$('#generateCloud').click(function() {

    event.preventDefault();

    var silloutte_path = $('#uploadImage').attr('src');
    var reddit_url = $('#reddit-url').val(); //get reddit url using id
    var text_input = $('#text_input').val(); //Get text data using id

    if(reddit_url==''&&text_input==''){ //check if input fields are empty

        alert('Please input a reddit comments url or some text!')

    };
    $.ajax({
        type: 'POST',
        url: '/process',
        data: JSON.stringify({ "path":silloutte_path, "reddit_url":reddit_url, "text_input":text_input } ),
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){

          status = data['message'] //check if success or error

          if(status=='success'){ //if success show new word cloud image
            my_url = "{{ url_for('upload', filename="+data['cloud_file_path']+" }}";
            $("#cloud_image").attr('src', data['cloud_file_path']); // setting the src attribute of img tag
            $("#img-download-btn").attr('value', data['cloud_file_path'])
            $("#file-download-btn").attr('value', data['csv_file_path'])
          }
          else if(status=='No data'){ //If reddit url incorrect or returned no data
            alert('Bad Reddit URL or issue connecting to Reddit.')
          }
          else{
            alert('Failed to generate word cloud.')
          };
    }).fail(function(data){
        alert('error!');
    });
});