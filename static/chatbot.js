$(document).ready(function() {
    $("#messageArea").on("submit", function(event){
        event.preventDefault();  
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour + ":" + minute;
        var rawText = $("#text").val();

        // Append user message
        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';
        $("#text").val("");  // Clear the input field
        $("#messageFormeight").append(userHtml);

        // Send message to the server
        $.ajax({
            type: "POST",
            url: "/get",
            data: JSON.stringify({ msg: rawText }),  // Send message as JSON
            contentType: "application/json",  // Correct content type
            success: function(data) {
                if (data.response) {
                    // Append bot response
                    var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + data.response + '<span class="msg_time">' + str_time + '</span></div></div>';
                    $("#messageFormeight").append(botHtml);
                }
            },
            error: function() {
                console.error("Error with the AJAX request.");
            }
        });
    });
});
