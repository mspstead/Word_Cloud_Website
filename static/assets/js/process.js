$('#run-button').click(function() {

    event.preventDefault();

    //Check which image mask is selected
    if($('input[name=upload-mask]:checked').val()!=null){
        var silloutte_path = $('input[name=upload-mask]:checked').val();
    }
    else{
        var silloutte_path = $('input[name=mask]:checked').val();
    };

    //Get text input option
    var text_input_option = $('input[name=text-options]:checked').val();

    //Get page_input_option for twitter search depth
    var page_input_option = $('input[name=page-options]:checked').val();

    //Get stats checked option
    var stats_selection='';
    if($('#show-stats').is(":checked")==true){
        stats_selection = 'checked';
    };

    //initialise scheme
    var selectedBackground = $("input[name='inlineColourOptions']:checked").val(); //get selected background colour
    var selectedScheme = $("input[name='ColourScheme']:checked").val(); //get selected colour scheme

    //initliase input
    var input = '';

    if(text_input_option=='comments' || text_input_option=='user' || text_input_option=='twitter'){
        input = $('#reddit-input').val();
    }
    else if(text_input_option=='raw'){
        input = $('#text-input').val();
    };

    if(input==''){ //check if input fields are empty
        alert('Please input a reddit comments url, username, or some text!')
    };

    var reddit_url = '';
    var user_name = '';
    var twitter_user = '';
    var text_input = '';

    $("#run-button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Creating...').prop('disabled',true);

    if(text_input_option=='comments'){
        reddit_url = input
    }
    else if(text_input_option=='user'){
        user_name = input
    }
    else if(text_input_option=='twitter'){
        twitter_user = input
    }
    else if(text_input_option=='raw'){
        text_input = input
    };
    $.ajax({
        type: 'POST',
        url: '/process',
        data: JSON.stringify({ "path":silloutte_path, "reddit_url":reddit_url, "user_name":user_name,"twitter":twitter_user,
        "text_input":text_input, "page_depth":page_input_option, 'stats_selection':stats_selection,
        "backgroundColour":selectedBackground, "colour_scheme":selectedScheme } ),
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){

          $("#run-button").html('Create Cloud!').prop('disabled',false);

          status = data['message'] //check if success or error

          if(status=='success'){ //if success show new word cloud image
            $("#cloud_image").attr('src', data['cloud_file_path']); // setting the src attribute of img tag
            $("#cloud-button").attr('value', data['cloud_file_path'])
            $("#stats-button").attr('value', data['csv_file_path'])
          }
          else if(status=='No data'){ //If reddit or twitter input incorrect or returned no data
            alert('Error: Cannot connect to reddit/twitter services.')
          };
    }).fail(function(data){
        $("#run-button").html('Create Cloud!').prop('disabled',false);
        alert('Error: Failed to create word cloud!');
    });
});