var lineType = "White";
var slidep = 50;
var slidei = 50;
var slided = 50;
var slideMin, slideMax = 50;

var slideValues = {
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

function getP() {
    return slidep;
}
function getI() {
    return slidei;
}
function getD() {
    return slided;
}
function getLineType() {
    if (lineType == "Black")
        return false;
    else 
        return lineType;
}
function getMinSpeed() {
    return slideMin;
}
function getMaxSpeed() {
    return slideMax;
}

module.exports = {
    getD,
    getI,
    getP,
    getLineType,
    getMinSpeed,
    getMaxSpeed
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
// console.log(exports);

// export {getP, getI, getD, getMaxSpeed, getMinSpeed, getLineType, LTGCarsUI};
