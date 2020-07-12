$("#info-button").click(function(){
    $("#info-modal").modal("show");
});
$("#shape-button").click(function(){
    $("#shape-modal").modal("show");
});
$("#colour-button").click(function(){
    $("#colours-modal").modal("show");
});
$("#input-button").click(function(){
    $("#input-modal").modal("show");
});
$('input:radio[name="text-options"]').change(function(){
    if($(this).val() == 'comments'){
        document.getElementById("input-type-label").innerHTML = "Input type: Reddit comments URL";
        document.getElementById("text-input").style.display = "none";
        document.getElementById("reddit-input").style.display = "block";
        document.getElementById("reddit-input").placeholder="Example: www.reddit.com/r/PrequelMemes/comments/hibtr6/something_stood_out_to_me_in_this_scene/"
        document.getElementById("depth-selection").style.display = "none";
    }
    else if($(this).val() == 'user'){
        document.getElementById("input-type-label").innerHTML = "Input type: Reddit username";
        document.getElementById("text-input").style.display = "none";
        document.getElementById("reddit-input").style.display = "block";
        document.getElementById("reddit-input").placeholder = "Example: spez"
        document.getElementById("depth-selection").style.display = "none";
    }
    else if($(this).val() == 'raw'){
        document.getElementById("input-type-label").innerHTML = "Input type: Raw text";
        document.getElementById("text-input").style.display = "block";
        document.getElementById("reddit-input").style.display = "none";
        document.getElementById("depth-selection").style.display = "none";
    }
    else if($(this).val() == 'twitter'){
        document.getElementById("input-type-label").innerHTML = "Input type: Twitter user";
        document.getElementById("text-input").style.display = "none";
        document.getElementById("reddit-input").style.display = "block";
        document.getElementById("reddit-input").placeholder = "Example: @realdonaldtrump or realdonaldtrump";
        document.getElementById("depth-selection").style.display = "block";
    };
});