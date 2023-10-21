const io = require('socket.io-client');
const socket = io.connect('http://localhost:5500');

socket.on('joint_coordinates', (data) => {
    const mouseX = data.x;
    const mouseY = data.y;

    const bubbles = document.querySelectorAll('.bubble');
    bubbles.forEach(bubble => {
        const rect = bubble.getBoundingClientRect();
        if (mouseX >=rect.left && mouseX <= rect.right && mouseY >= rect.top && mouseY <= rect.bottom) {
            bubble.remove();
        }
    });
});

function createBubble() {
    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    //random size
    const size = Math.floor(Math.random() * 50) + 20;
    bubble.style.width = size + 'px';
    bubble.style.height = size + 'px';

    //random position
    const maxX = window.innerWidth - size;
    const maxY = window.innerHeight - size;
    bubble.style.left = Math.random() * maxX + 'px';
    bubble.style.top = Math.random() * maxY + 'px';

    document.getElementById('game-container').appendChild(bubble);
}

setInterval(createBubble, 1000);