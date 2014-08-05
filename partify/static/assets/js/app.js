$(document).ready(function(){

    function addEntryTwitter(entry) {
      var template = $('#twitter-entry-template').html();
      var rendered = Mustache.render(template, entry);
      $('#stream').prepend(rendered);
    }


    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stream');

    // Define on connect data
    socket.on('connect', function() {
        console.log("Client connected to server via socketio.");
    });

    // Define on connect data
    socket.on('disconnect', function() {
        console.log("Socketio client disconnected to server.");
    });

    /*
     Status Event.
     */
    socket.on('status', function(msg) {
        $('#log').append('<p>Received: ' + msg.data + '</p>');
    });

    /*
     Twitter Event.
     */
    socket.on('stream-data-twitter', function(msg) {

        // Add Entry from a mustache template.
        addEntryTwitter({
            socialtype: "Twitter",
            name: msg.data.screen_name,
            sharemessage: "Shared on Twitter",
            date: moment().format("MMM Do YY"),
            textmessage: msg.data.text,
            profile_image_url: msg.data.profile_image_url
        });

    });

    /*
     Instagram Event.
     */
    socket.on('stream-data-instagram', function(msg) {
        $('#stream').prepend('<p>'+msg.data.name+': ' + msg.data.text + '</p>');
    });

    // Handle enter event when menu is open
    $(document).keypress(function (e) {

        // If the key is "ENTER"
        if (e.which == 13) {

            // Prevent enter button from being pressed.
            e.preventDefault();

            if($('#search').val() != "") {
                socket.emit('start-stream', {'tracking': [$('#search').val()]});
            }
            else
                alert("No search string to track");

        }
    });

    $('.panel-google-plus > .panel-footer > .input-placeholder, .panel-google-plus > .panel-google-plus-comment > .panel-google-plus-textarea > button[type="reset"]').on('click', function(event) {
        var $panel = $(this).closest('.panel-google-plus');
            $comment = $panel.find('.panel-google-plus-comment');

        $comment.find('.btn:first-child').addClass('disabled');
        $comment.find('textarea').val('');

        $panel.toggleClass('panel-google-plus-show-comment');

        if ($panel.hasClass('panel-google-plus-show-comment')) {
            $comment.find('textarea').focus();
        }
   });
   $('.panel-google-plus-comment > .panel-google-plus-textarea > textarea').on('keyup', function(event) {
        var $comment = $(this).closest('.panel-google-plus-comment');

        $comment.find('button[type="submit"]').addClass('disabled');
        if ($(this).val().length >= 1) {
            $comment.find('button[type="submit"]').removeClass('disabled');
        }
   });

});

