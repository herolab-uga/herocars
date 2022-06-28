// https://blog.idrisolubisi.com/how-to-integrate-real-time-webcam-on-a-web-page-using-javascript
// sliders for p, i, d
// sliders for min and max
// big camera view
// button to switch control modes
// button to switch line types

function startLTGCars() {
    // ip address and stuff and connect button
    LTGCarsArea.start();
}

var LTGCarsArea = { // to canvas or no canvas 
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 600;
        this.canvas.height = 300;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.frameNo = 0;
        // this.interval = setInterval(updateCarImg, 20); update to socket, probably not 20 seconds
        },
    clear : function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

var Movement = {
    right: function() {

    },
    left: function() {

    },
    forward: function() {

    },
    backward: function() {
        
    }
}

function updateCarIMG () {
    // just something to update the image received from the car
}

function updateCarPlacement() {

    node.addEventListener('keydown', function(event) {
        const key = event.key; // "ArrowRight", "ArrowLeft", "ArrowUp", or "ArrowDown"
        if (key == "ArrowRight")
            Movement.right();
        if (key == "ArrowLeft")
            Movement.left();
    });
}

function disableButtons() {
    // disable buttons if connection is lost.
    // check for enabling.
}