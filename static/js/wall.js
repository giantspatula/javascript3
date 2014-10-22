$(document).ready(function () {
    // Normally, JavaScript runs code at the time that the <script>
    // tags loads the JS. By putting this inside a jQuery $(document).ready()
    // function, this code only gets run when the document finishing loading.
    // loadmessages();
    loadMessagesHTML();
    $("#message-form").submit(handleFormSubmit);
    $("#messages-clear").click(handleClearButton);
});


/**
 * Handle submission of the form.
 */
function handleFormSubmit(evt) {
    evt.preventDefault();

    var textArea = $("#message");
    var msg = textArea.val();

    // if($("#message-form").prop("disabled"))
    //     {  do nothing }
    // else
    //     $("#message-form").prop("disabled", true)
    //     setTimeout(function(){
    //         $("#message-form").prop("disabled", false)
    //     }, 5000)
    // setTimeout(function () {
    //     alert("please wait a moment before your next msg")
    //     }, 2000);

    console.log("handleFormSubmit: ", msg);
    addMessage(msg);

    // Reset the message container to be empty
    textArea.val("");
    
    
}

function handleClearButton(evt) {
    evt.preventDefault();
    console.log("clicked on reset button")
    $.post(
        "/api/wall/reset",
        {},
         function(data){
            console.log('handleClearButton got: ');
            console.log(data);
            if (data.result == 'OK') {
                //alert("GOT THIS FAR!");
                $("#message-container").empty();
                loadmessages();
            }
         }
        )
}

/**
 * Makes AJAX call to the server and the message to it.
 */
function addMessage(msg) {
    $.post(
        "/api/wall/add",
        {'m': msg, 'datetime': $.now()},
        function (data) {
            console.log("addMessage: ", data);
            displayResultStatus(data.result);
            if (data.result === "failure")
            {
                alert("Wait 5 seconds between posting messages.")
            }
            else
            {
                $("#message-container").empty();
                loadmessages();
            }
            
        }
    );
}


/**
 * This is a helper function that does nothing but show a section of the
 * site (the message result) and then hide it a moment later.
 */
function displayResultStatus(resultMsg) {
    var notificationArea = $("#sent-result");
    notificationArea.text(resultMsg);
    notificationArea.slideDown(function () {
        // In JavaScript, "this" is a keyword that means "the object this
        // method or function is called on"; it is analogous to Python's
        // "self". In our case, "this" is the #sent-results element, which
        // is what slideDown was called on.
        //
        // However, when setTimeout is called, it won't be called on that
        // same #sent-results element--"this", for it, wouldn't be that
        // element. We could put inside of our setTimeout call the code
        // to re-find the #sent-results element, but that would be a bit
        // inelegant. Instead, we'll use a common JS idiom, to set a variable
        // to the *current* definition of self, here in this outer function,
        // so that the inner function can find it and where it will have the
        // same value. When stashing "this" into a new variable like that,
        // many JS programmers use the name "self"; some others use "that".
        var self = this;

        setTimeout(function () {
            $(self).slideUp();
        }, 2000);
    });
}

function loadmessages(){

    
    $.get("/api/wall/list.json", function(request_object)
    {
      console.log(request_object["messages"]);
      for(var i = 0; i < request_object["messages"].length; i++)
      {
        post_message = "<li class='list-group-item'>" + request_object["messages"][i].message + "</li>";
        $("#message-container").append(post_message);
      }
    });
}

function loadMessagesHTML() {
    $('#message-container').load('/api/wall/list.html');
}