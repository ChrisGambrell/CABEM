//required modules
const express = require('express')
const app = express()
const morgan = require('morgan')
const bodyParser = require('body-parser')
var AWS = require("aws-sdk");
var uuid = require('uuid');
var fs = require('fs');
var path = require('path');

app.use(bodyParser.urlencoded({ extended: false }))
app.use(express.static('.')) //loads html file
app.use(morgan('short'))

//configure credentials
var credentials = new AWS.SharedIniFileCredentials({ profile: 'team11_aws' });
AWS.config.credentials = credentials;
AWS.config.update({ region: 'us-east-2' });

//test credentials
AWS.config.getCredentials(function (err) {
    if (err) console.log(err.stack);
    // credentials not loaded
    else {
        console.log("Access key:", AWS.config.credentials.accessKeyId);
    }
});
console.log("Region: ", AWS.config.region);
console.log("Host: ", AWS.config.host);

// Create S3 service object
s3 = new AWS.S3({ apiVersion: '2006-03-01' });//required modules

app.post('/user_create', (req, res) => {
    console.log("First name: " + req.body.create_first_name)
    console.log("Last name: " + req.body.create_last_name)
    const firstName = req.body.create_first_name
    const lastName = req.body.create_last_name
})

app.get("/", (req, res) => {
    console.log("Responding to root route")
    res.send("Hello from root!")
})

// localhost:3003
app.listen(3003, () => {
    console.log("Server is up and listening on 3003...")
})

//------------------Creates Bucket------------------//
app.post("/create_bucket", (req, res) => {
    console.log("Creating Random Bucket")
    // Create unique bucket name
    var bucketName = 'node-sdk-sample-' + uuid.v4();
    // Create a promise on S3 service object
    var bucketPromise = s3.createBucket({ Bucket: bucketName }).promise();
    res.send("Random Bucket Created")
})
//--------------Add Custom Named Bucket-------------//
app.post("/custom_bucket", (req, res) => {
    console.log("Creating Custom Bucket")
    s3.createBucket({
        Bucket: `${req.body.custom_bucket_name}`
    }).promise();
    res.send("Custom Bucket Created")
})
//------------------Add to Bucket-------------------//
app.post("/add_test_file_to_bucket", (req, res) => {
    console.log("Adding test_file.txt to " + req.body.test_bucket_name)
    s3.putObject({
        Bucket: `${req.body.test_bucket_name}`,
        Key: 'test_file.txt',
        Body: 'Hello World!' 
    }).promise();
    res.send("Added test_file.txt to " + req.body.test_bucket_name)
})

//-------------------List Buckets-------------------//
app.get("/list_buckets", (req, res) => {
    console.log("Listing Buckets")
    s3.listBuckets(function (err, data) {
        if (err) {
            res.send(err)
        } else {
            res.send(data.Buckets)
        }
    });
})

//----------------Upload File to Bucket-------------// NOT DONE
app.post("/upload_to_bucket", (req, res) => {
    console.log("Upload time")

    var uploadParams = { 
        Bucket: req.body.bucket_to_upload, 
        Key: '', 
        Body: '' 
    };
    var file = req.body.file_to_upload;

    // Configure the file stream and obtain the upload parameters
    var fileStream = fs.createReadStream(file);
    fileStream.on('error', function (err) {
        console.log('File Error', err);
    });
    uploadParams.Body = fileStream;
    uploadParams.Key = path.basename(file);

    // call S3 to retrieve upload file to specified bucket
    s3.upload(uploadParams, function (err, data) {
        if (err) {
            console.log("Error", err);
        } if (data) {
            console.log("Upload Success", data.Location);
        }
    });

    res.send("Hello from root!")
})

//----------------List Objs in a Bucket-------------//
app.post("/list_objs_in_bucket", (req, res) => {
    console.log("Listing Objs in " + req.body.list_bucket_name)
    s3.listObjects({ Bucket: `${req.body.list_bucket_name}` }, function (err, data) {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
})

//--------------------Delete Bucket-----------------//
app.post("/delete_empty_bucket", (req, res) => {
    console.log("Deleting Bucket: " + req.body.delete_bucket_name)
    s3.deleteBucket({ Bucket: `${req.body.delete_bucket_name}` }, function (err, data) {
        if (err) {
            res.send(err);
        } else {
            res.send("Deleted Bucket: " + req.body.delete_bucket_name);
        }
    });
})

/*
var http = require('http');
var fs = require('fs');

var server = http.createServer(function (req, res) {
    console.log('request was made: '+ req.url);
    res.writeHead(200, { 'Content-Type': 'text/html' });
    var myReadStream = fs.createReadStream(__dirname + '/index.html', 'utf-8');
    myReadStream.pipe(res);
});

var serverPort = 8080
server.listen(serverPort);
console.log('Now listening to port ' + serverPort);
console.log('Ctrl + C to end server');

function myFunction() {
    console.log("This function worked");
}
*/