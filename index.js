import * as express from 'express';
// import app from '../app';
import * as http from 'http';
import * as Net from 'net';
import path from 'path';
import * as ltgcars from './LTGCarsUI.cjs';

const app = express();              
const port = 5001;                  
var server = http.Server(app);

// allows html, style sheets, and other images to send to server
// app.use(express.static(path.join(__dirname, '/'))); 

// from LTGCarsUI.js
// const ltgcars = require('LTGCarsUI');
// var p, i, d, minSpeed, maxSpeed = 50;
// var lineType = true;

var d = ltgcars.getD();
console.log("D" + d);

//Idiomatic expression in express to route and respond to a client request
app.get('/', (req, res) => { 
    res.sendFile('index.html', {root: __dirname});      //server responds by sending the index.html file to the client's browser 
});

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});


// Include Nodejs' net module.
// const Net = require('net');
const host = '127.0.0.1';

const port_control = 5000;

const client = Net.createConnection({ port: port_control }, () => {
    // 'connect' listener.
    console.log('connected to server!');
    setInterval(() => {
        updateAll();
    }, 1000);
    
    function updateAll() {
        console.log(ltgcars.getP); // still undefined
        console.log(ltgcars.p);
        if (p != ltgcars.getP()) {
            p = ltgcars.getP();
            
            client.write(1);
            client.write(p);
        }
        if (i != ltgcars.getI()) {
            i = ltgcars.getI();
            client.write(2);
            client.write(i);
        }
        if (d != ltgcars.getD()) {
            d = ltgcars.getD();
            client.write(3);
            client.write(d);
        }
        if (minSpeed != ltgcars.getMinSpeed()) {
            minSpeed = ltgcars.getMinSpeed();
            client.write(5);
            client.write(minSpeed);
        }
        if (maxSpeed != ltgcars.getMaxSpeed()) {
            maxSpeed = ltgcars.getMaxSpeed();
            client.write(6);
            client.write(maxSpeed);
        }
        if (lineType != ltgcars.getLineType()) { // white is true
            lineType = ltgcars.getLineType();
            client.write(8);
            client.write(lineType)
        }
    }
  });

// The client can also receive data from the server by reading from its socket.
client.on('data', function(chunk) {
    console.log(`Data received from the server: ${chunk.toString()}.`);
    
    // Request an end to the connection after the data has been received.
    client.end();
});

client.on('end', function() {
    console.log('Requested an end to the TCP connection');
});
