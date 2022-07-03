const express = require('express'); 
const app = express();              
const port = 5000;                  
var server = require('http').Server(app);
var io = require('socket.io')(server);

const path = require('path');
app.use(express.static(path.join(__dirname, '/')));


const ltgcars = require("./LTGCarsUI");
var p, i, d, minSpeed, maxSpeed = 50;
var lineType = true;



//Idiomatic expression in express to route and respond to a client request
app.get('/', (req, res) => {        //get requests to the root ("/") will route here
    res.sendFile('index.html', {root: __dirname});      //server responds by sending the index.html file to the client's browser
                                                        //the .sendFile method needs the absolute path to the file, see: https://expressjs.com/en/4x/api.html#res.sendFile 
});

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});


// Include Nodejs' net module.
const Net = require('net');
// The port number and hostname of the server.
const host = 'localhost';

const client = new Net.Socket();

client.connect({ port: port, host: host }), function() {
    console.log('TCP connection established with the server.');

    
    client.write('server on');

    setInterval(() => {
        updateAll();
    }, 1000);
    
    function updateAll() {
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
    
    

};

// The client can also receive data from the server by reading from its socket.
client.on('data', function(chunk) {
    console.log(`Data received from the server: ${chunk.toString()}.`);
    
    // Request an end to the connection after the data has been received.
    client.end();
});

client.on('end', function() {
    console.log('Requested an end to the TCP connection');
});