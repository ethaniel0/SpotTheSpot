var socket = io();
    
socket.on('img', ({image}) => {
    img = image;
    document.getElementById('picture').src = image;
};