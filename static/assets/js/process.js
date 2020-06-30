$('#run-button').click(function() {

    event.preventDefault();

    //Check which image mask is selected
    var silloutte_path = $('input[name=mask]:checked').val();

    //Get text input option
    var text_input_option = $('input[name=text-options]:checked').val();

    //initialise scheme
    var selectedBackground = $("input[name='inlineColourOptions']:checked").val(); //get selected background colour
    var selectedScheme = $("input[name='ColourScheme']:checked").val(); //get selected colour scheme

    //initliase input
    var input = ''

    if(text_input_option=='comments' || text_input_option=='user'){
        input = $('#reddit-input').val();
    }
    else if(text_input_option=='raw'){
        input = $('#text-input').val();
    };

    if(input==''){ //check if input fields are empty
        alert('Please input a reddit comments url, username, or some text!')
    };

    var reddit_url = ''
    var user_name = ''
    var text_input = ''

    $("#run-button").html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Running...').addClass('disabled');

    if(text_input_option=='comments'){
        reddit_url = input
    }
    else if(text_input_option=='user'){
        user_name = input
    }
    else if(text_input_option=='raw'){
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

          $("#run-button").html('Run').addClass('enabled')

          status = data['message'] //check if success or error

          if(status=='success'){ //if success show new word cloud image
            $("#cloud_image").attr('src', data['cloud_file_path']); // setting the src attribute of img tag
            $("#cloud-button").attr('value', data['cloud_file_path'])
            $("#stats-button").attr('value', data['csv_file_path'])
          }
          else if(status=='No data'){ //If reddit url incorrect or returned no data
            alert('Bad Reddit URL/Username or issue connecting to Reddit.')
          };
    }).fail(function(data){
        $("#generateCloud").html('Generate Word Cloud').addClass('enabled')
        alert('Error: Failed to create word cloud!');
    });
});