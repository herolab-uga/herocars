import * as bg from './index.js';
var lineType = "White";
var slidep = 50;
var slidei = 50;
var slided = 50;
var slideMin, slideMax = 50;

if (typeof window !== 'undefined') {
    let p = document.getElementById("pRange");
    let i = document.getElementById("iRange");
    let d = document.getElementById("dRange");
    let minSpeed = document.getElementById("minSpeed");
    let maxSpeed = document.getElementById("maxSpeed");
    let button = document.querySelector("button");

    button.addEventListener('click', function(e) {
        console.log('button was clicked');
    });


    p.oninput = function() {
        slidep = p.value;
        console.log("HI"+slidep);
        bg.updateP(slidep);
    }
    i.onchange = function() {
        slidei = i.value;
    }
    d.onchange = function() {
        slided = d.value;
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

// module.exports = {
//     getD,
//     getI,
//     getP,
//     getLineType,
//     getMinSpeed,
//     getMaxSpeed,
//     changeLineType,
//     lineType,
//     slideValues,
// }
