document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('input').forEach(button => {
            button.onclick = () => {
                socket.emit('reviews',data);
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('submit review', data => {
        document.querySelector('#reviewer').innerHTML = data.reviewer;
        document.querySelector('#review_date').innerHTML = data.review_date;
        document.querySelector('#review').innerHTML = data.maybe;
    });
});
