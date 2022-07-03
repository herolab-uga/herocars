// https://blog.idrisolubisi.com/how-to-integrate-real-time-webcam-on-a-web-page-using-javascript

// big camera view

var lineType = "White"; // set to white

function start() {
    if (enableButtons( ) == true) {
        console.log("Program Started");
        setInterval(updateCarIMG(), 1000);
    } else {
        // disable buttons
    }
    
}

var slideValues = { // these are received from LTGCarsApp at slider script oninput
    p: function(value) {
        console.log(value);
    },
    i: function(value) {
        console.log(value);
    },
    d: function(value) {
        console.log(value);
    },
    minSpeed: function(value) {
        console.log(value);
    },
    maxSpeed: function(value) {
        console.log(value);
    }
}

function changeLineType() {
    if (lineType == "Black") {
        lineType = "White";
    } else {
        lineType = "Black";
    }
    console.log("Line Type Changed To : " + lineType);
}

var Movement = { // received from button pushes on input
    right: function() {
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
    // updates the image received from the car
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