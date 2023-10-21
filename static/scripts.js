

// var socket = io.connect('http://' + document.domain + '.' + location.port);
// var score = 0;

// function updateScore() {
//     document.getElementById('score').innerText = 'Score: '  + score;
// }


// socket.on('pose_data', function(data) {

//     console.log('Received pose data:', data);
    
//     var rightPalmX = data.rightPalm_x;
//     var rightPalmY = data.rightPalm_y
//     var bubbleContainer = document.getElementById('bubble-container');
//     var bubbleSize = 50;
//     var bubbleSpeed = 2;
//     var collisionThreshold = 25;

//     if (Math.random() < 0.01) {
//         var bubble = document.createElement('div');
//         bubble.className = 'bubble';
//         bubble.style.width = bubbleSize + 'px';
//         bubble.style.height = bubbleSize + 'px';
//         bubble.style.left = Math.random() * (window.innerWidth - bubbleSize) + 'px';
//         bubble.style.top = '0px';
//         bubbleContainer.appendChild(bubble);
//     }

//     var bubbles = document.querySelectorAll('.bubble');
//     bubbles.forEach(function(bubble) {
//         var bubbleY = parseInt(bubble.style.top);
//         bubbleY += bubbleSpeed;
//         bubble.style.top = bubbleY + 'px';

//         var bubbleX = parseInt(bubble.style.left) + bubbleSize / 2;
//         var bubbleYCenter = bubbleY + bubbleSize / 2;
//         var distance = Math.sqrt(Math.pow(rightPalmX - bubbleX, 2) + Math.pow(rightPalmY - bubbleYCenter, 2));

//         if (distance < collisionThreshold){
//             bubble.remove();
//             score ++;
//             updateScore();
//         }

//         if(bubbleY > window.innerHeight) {
//             bubble.remove();
//         }

//     });
// });
    

// updateScore();
