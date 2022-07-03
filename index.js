import express from 'express';
import http from 'http';
import Net from 'net';
import path from 'path';
import ltgcars from './LTGCarsUI.cjs';
import {fileURLToPath} from 'url';

const app = express();              
const port = 5001;                  
var server = http.Server(app); 
const host = '127.0.0.1';

const port_control = 5000;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const publicDirectoryPath = path.join(__dirname, '/');
app.use(express.static(path.join(publicDirectoryPath)));


var p, i, d, minSpeed, maxSpeed = 50;
var lineType = true;

//Idiomatic expression in express to route and respond to a client request
app.get('/', (req, res) => { 
    res.sendFile('index.html', {root: __dirname});      //server responds by sending the index.html file to the client's browser 
});

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});


const client = Net.createConnection({ port: port_control }, () => {
    // 'connect' listener.
    console.log('connected to server!');
    setInterval(() => {
        updateAll();
    }, 1000);
    
    function updateAll() {
        var keyCode;
        var keyVal;
        
        if (p != ltgcars.getP()) {
            p = ltgcars.getP();
            keyCode = Buffer("1".toString(), "ascii");
            keyVal = Buffer(p.toString(), "ascii");
            client.write(keyCode);
            client.write(keyVal);
        }
        if (i != ltgcars.getI()) {
            i = ltgcars.getI();
            keyCode = Buffer("2".toString(), "ascii");
            keyVal = Buffer(i.toString(), "ascii");
            client.write(keyCode);
            client.write(keyVal);  
        }
        if (d != ltgcars.getD()) {
            d = ltgcars.getD();
            keyCode = Buffer("3".toString(), "ascii");
            keyVal = Buffer(d.toString(), "ascii");
            client.write(keyCode);
            client.write(keyVal);
        }
        if (minSpeed != ltgcars.getMinSpeed()) {
            minSpeed = ltgcars.getMinSpeed();
            keyCode = Buffer("5".toString(), "ascii");
            keyVal = Buffer(minSpeed.toString(), "ascii");
            client.write(keyCode);
            client.write(keyVal);
        }
        if (maxSpeed != ltgcars.getMaxSpeed()) {
            maxSpeed = ltgcars.getMaxSpeed();
            keyCode = Buffer("6".toString(), "ascii");
            keyVal = Buffer(maxSpeed.toString(), "ascii");
            client.write(keyCode);
            client.write(keyVal);
        }
        if (lineType != ltgcars.getLineType()) { // white is true
            lineType = ltgcars.getLineType();
            keyCode = Buffer("8".toString(), "ascii");
            keyVal = Buffer(lineType, "ascii");
            client.write(keyCode);
            client.write(keyVal);
        }
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
