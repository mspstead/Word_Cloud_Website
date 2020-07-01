document.querySelector('.custom-file-input').addEventListener('change',function(e){
    var fileName = document.getElementById("image").files[0].name;
    var nextSibling = e.target.nextElementSibling;
    nextSibling.innerText = fileName;
});
$(window).on('load',function() {
    event.preventDefault();

    $("#row-img-mask").html('<div class="col-md-4" id="col-img-1"></div><div class="col-md-4" id="col-img-2"></div><div class="col-md-4" id="col-img-3"></div>')

    $.ajax({
        type: 'GET',
        url: '/imageMasks',
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data){

          image_paths = data['image_paths']; //check if success or error

          var num_images_per_col = Math.ceil(image_paths.length/3);
          var col_1_count = num_images_per_col;
          var col_2_count = num_images_per_col;
          var col_3_count = num_images_per_col;

          for(var path of image_paths){
            if(col_1_count!=0){
                if(col_1_count==num_images_per_col){
                    var img = '<label><input type="radio" name="mask" value='+path+' checked><img class="img-fluid" src='+path+'></label>'
                }
                else{
                    var img = '<label><input type="radio" name="mask" value='+path+'><img class="img-fluid" src='+path+'></label>'
                };
                $('#col-img-1').append(img);
                col_1_count = col_1_count - 1
            }
            else if(col_2_count!=0){
                var img = '<label><input type="radio" name="mask" value='+path+'><img class="img-fluid" src='+path+'></label>'
                $('#col-img-2').append(img);
                col_2_count = col_2_count - 1
            }
            else if(col_3_count!=0){
                var img = '<label><input type="radio" name="mask" value='+path+'><img class="img-fluid" src='+path+'></label>'
                $('#col-img-3').append(img);
                col_3_count = col_3_count - 1
            };
          };

          $('input:radio[name="mask"]').change(function(){
             console.log('checked');
             $('input:radio[name="upload-mask"]').prop('checked',false);

          });

    }).fail(function(data){
        alert('Error: Failed to get image masks!');
    });
});
