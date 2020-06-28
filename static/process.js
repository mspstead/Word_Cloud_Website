$('#generateCloud').click(function() {

    event.preventDefault();

    var silloutte_path = $('#uploadImage').attr('src');
    var input = $('#text_input').val(); //Get text data using id

    var reddit_url = ''
    var user_name = ''
    var text_input = ''

    if(input==''){ //check if input fields are empty
        alert('Please input a reddit comments url, username, or some text!')
    };

    var selectedOption = $("input[name='inlineRadioOptions']:checked").val(); //get selected input option
    var selectedBackground = $("input[name='inlineColourOptions']:checked").val(); //get selected background colour
    var selectedScheme = $("input[name='ColourScheme']:checked").val(); //get selected colour scheme

    $("#generateCloud").html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Generating...').addClass('disabled');

    if(selectedOption=='option1'){
        reddit_url = input
    }
    else if(selectedOption=='option2'){
        user_name = input
    }
    else if(selectedOption=='option3'){
        text_input = input
    };
    $.ajax({
        type: 'POST',
        url: '/process',
        data: JSON.stringify({ "path":silloutte_path, "reddit_url":reddit_url, "user_name":user_name,
        "text_input":text_input, "backgroundColour":selectedBackground, "colour_scheme":selectedScheme } ),
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){

          $("#generateCloud").html('Generate Word Cloud').addClass('enabled')

          status = data['message'] //check if success or error

          if(status=='success'){ //if success show new word cloud image
            my_url = "{{ url_for('upload', filename="+data['cloud_file_path']+" }}";
            $("#cloud_image").attr('src', data['cloud_file_path']); // setting the src attribute of img tag
            $("#img-download-btn").attr('value', data['cloud_file_path'])
            $("#file-download-btn").attr('value', data['csv_file_path'])
          }
          else if(status=='No data'){ //If reddit url incorrect or returned no data
            alert('Bad Reddit URL/Username or issue connecting to Reddit.')
          };
    }).fail(function(data){
        $("#generateCloud").html('Generate Word Cloud').addClass('enabled')
        alert('Error: Failed to create word cloud!');
    });
});