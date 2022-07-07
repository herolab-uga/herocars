
import { createConnection } from "net";
import * as ltgcars from "../herocars/LTGCarsUI.js";
import path from 'path';
import {fileURLToPath} from 'url';
import express from "express";
var app = express();

           
const port = 5001;                  
const host = '127.0.0.1';

const port_control = 5000;

const __filename = fileURLToPath(import.meta.url);

const __dirname = path.dirname(__filename);
// console.log(path.join(__dirname, '/dist', 'index.html'));


app.use(express.static(__dirname + '/'));

app.get('/', function (req, res) {
    res.sendFile('index.html');
});


app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});


var lineType = "White";
var p = 50;
var newP = 0;
var i = 50;
var d = 50;

function updateP(val) {
    if (val != undefined) {
        console.log("new p " + val);
        newP = val;
    }
}

var minSpeed, maxSpeed = 50;

const client = createConnection({ port: port_control }, () => {
    // 'connect' listener.
    console.log('connected to server!');
    setInterval(() => {
        updateP(ltgcars.slidep);
        updateAll();
    }, 1000);


    function updateAll() {
        var keyCode;
        var keyVal;

        if (p != newP) {
            console.log("current p " + p);
            p = newP;
            console.log("new p " + p);
            keyCode = Buffer("1", "ascii");
            keyVal = Buffer(p.toString(), "ascii");
            client.write(keyCode);
            client.write(keyVal);
        }
        // if (i != slideValues.getI()) {
        //     i = slideValues.getI();
        //     keyCode = Buffer("2", "ascii");
        //     keyVal = Buffer(i.toString(), "ascii");
        //     client.write(keyCode);
        //     client.write(keyVal);  
        // }
        // if (d != slideValues.getD()) {
        //     d = slideValues.getD();
        //     keyCode = Buffer("3", "ascii");
        //     keyVal = Buffer(d.toString(), "ascii");
        //     client.write(keyCode);
        //     client.write(keyVal);
        // }
        // if (minSpeed != ltgcars.getMinSpeed()) {
        //     minSpeed = ltgcars.getMinSpeed();
        //     keyCode = Buffer("5".toString(), "ascii");
        //     keyVal = Buffer(minSpeed.toString(), "ascii");
        //     client.write(keyCode);
        //     client.write(keyVal);
        // }
        // if (maxSpeed != ltgcars.getMaxSpeed()) {
        //     maxSpeed = ltgcars.getMaxSpeed();
        //     keyCode = Buffer("6".toString(), "ascii");
        //     keyVal = Buffer(maxSpeed.toString(), "ascii");
        //     client.write(keyCode);
        //     client.write(keyVal);
        // }
        // if (lineType != ltgcars.getLineType()) { // white is true
        //     lineType = ltgcars.getLineType();
        //     keyCode = Buffer("8".toString(), "ascii");
        //     keyVal = Buffer(lineType, "ascii");
        //     client.write(keyCode);
        //     client.write(keyVal);
        // }
    }
  });

// The client can also receive data from the server by reading from its socket.
// client.on('data', function(chunk) {
//     console.log(`Data received from the server: ${chunk.toString()}.`);
    
//     // Request an end to the connection after the data has been received.
//     client.end();
// });

client.on('end', function() {
    console.log('Requested an end to the TCP connection');
});
