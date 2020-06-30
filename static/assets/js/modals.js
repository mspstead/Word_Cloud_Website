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
    }
    else if($(this).val() == 'user'){
        document.getElementById("input-type-label").innerHTML = "Input type: Reddit username";
        document.getElementById("text-input").style.display = "none";
        document.getElementById("reddit-input").style.display = "block"; 
    }
    else if($(this).val() == 'raw'){
        document.getElementById("input-type-label").innerHTML = "Input type: Raw text";
        document.getElementById("text-input").style.display = "block";
        document.getElementById("reddit-input").style.display = "none";
    };
});