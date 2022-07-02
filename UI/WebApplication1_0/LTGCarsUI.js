// https://blog.idrisolubisi.com/how-to-integrate-real-time-webcam-on-a-web-page-using-javascript

// big camera view
// button to switch control modes
// button to switch line types

var p = document.getElementById("pRange");
var i = document.getElementById("iRange");
var d = document.getElementById("dRange");
var min = document.getElementById("min");
var max = document.getElementById("max");

var pValToPrint = document.getElementById("pPrint"); // to show user
var iValToPrint = document.getElementById("iPrint");
var dValToPrint = document.getElementById("dPrint");
var minToPrint = document.getElementById("min");
var maxToPrint = document.getElementById("max");

function start() {
    if (enableButtons( ) == true) {
        console.log("Program Started");
        setInterval(updateCarIMG(), 1000);
    } else {
        // disable buttons
    }
    
}

var Movement = {
    right: function() {
        // send message to car to move 
        console.log("Moving right");
    },
    left: function() {
        console.log("Moving left");
    },
    forward: function() {
        console.log("Moving forward");
    },
    backward: function() {
        console.log("Moving backward");
    }
}

function updateCarIMG () {
    // just something to update the image received from the car
    console.log("Image updated");
}

// updates car's placement from up and down arrow keys & buttons on webpage
function updateCar() {

    node.addEventListener('keydown', function(event) {
        const key = event.key;
        if (key == "ArrowRight")
            Movement.right();
        if (key == "ArrowLeft")
            Movement.left();
        if (key == "ArrowUp")
            Movement.forward();
        if (key == "ArrowDown")
            Movement.backward();
    });
}

function enableButtons() {
    return true;
    // disable buttons if connection is lost.
    // check for enabling.
}