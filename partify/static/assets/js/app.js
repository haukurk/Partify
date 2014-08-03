$(document).ready(function(){

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
        $('#stream').prepend('<p>'+msg.data.screen_name+': ' + msg.data.text + '</p>');
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

});

