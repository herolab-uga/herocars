// https://blog.idrisolubisi.com/how-to-integrate-real-time-webcam-on-a-web-page-using-javascript

// big camera view

var lineType = "White"; // set to white
var slidep = 50;
var slidei = 50;
var slided = 50;
var slideMin, slideMax = 50;

var slideValues = { // these are received from LTGCarsApp at slider script oninput
    p: function(value) {
        slidep = value;
        // console.log(slidep);
    },
    i: function(value) {
        slidei = value;
    },
    d: function(value) {
        slided = value;
    },
    minSpeed: function(value) {
        slideMin = value;
    },
    maxSpeed: function(value) {
        slideMax = value;
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
modules.export = {

    getP: function() {
        return slidep;
    },
    getI: function() {
        return slidei;
    },
    getD: function() {
        return slided;
    },
    getLineType: function() {
        if (lineType == "Black")
            return false;
        else 
            return lineType;
    },
    getMinSpeed: function() {
        return minSpeed;
    },
    getMaxSpeed: function() {
        return maxSpeed;
    }
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

// export {getP, getI, getD, getMaxSpeed, getMinSpeed, getLineType, LTGCarsUI};
