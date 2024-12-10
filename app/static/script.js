// Display Options Sidebar
function openBar() {
    document.getElementById("contain").style.gridTemplateColumns = 'repeat(3, 1fr)';
    document.getElementById("sidebar").style.display = "block";
}

function closeBar() {
    document.getElementById("contain").style.gridTemplateColumns = '1fr 1fr';
    document.getElementById("sidebar").style.display = "none";
}

//Like and Dislike Function
$(document).ready(function() {

    // Set the CSRF token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetupso that the CSRF token is added to the header of every request
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("button.likes, button.dislikes").on("click", function() {
        // Get Both Button Objects
        var btn = $(this);
        msg_id = btn.attr("id");
        action = btn.attr("action");
        if (btn.attr('class') == "likes"){
            var btn_1 = document.querySelector('button.likes[id="'+msg_id+'"]');
            var btn_2 = document.querySelector('button.dislikes[id="'+msg_id+'"]');
        }
        else if (btn.attr('class') == "dislikes")
        {
            var btn_1 = document.querySelector('button.dislikes[id="'+msg_id+'"]');
            var btn_2 = document.querySelector('button.likes[id="'+msg_id+'"]');
        }
        // Request to update record
            $.ajax({
                url: '/update_likes',
                type: 'POST',
                //Send Message ID, 
                data: JSON.stringify({ id: msg_id, action: action}),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                // Display the new likes and dislike number - Once per User
                success: function(response){
                    console.log(response);
                    //User pressed Likes
                    if (action == "like")
                    {
                        btn_1.innerHTML = '<i class="fa fa-thumbs-up"></i>' + response.likes;
                        btn_2.innerHTML = '<i class="fa fa-thumbs-down"></i>' + response.dislikes;
                    }
                    else if (action == "dislike")
                    {       
                        btn_1.innerHTML = '<i class="fa fa-thumbs-down"></i>' + response.dislikes;
                        btn_2.innerHTML = '<i class="fa fa-thumbs-up"></i>' +response.likes;
                    }
                },
                // Failed
                error: function(error) {
                    console.log(error);
                }
        });
    });
});
