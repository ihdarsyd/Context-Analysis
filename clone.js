const mongo = require('mongodb').MongoClient
var url = "mongodb://localhost:27017/";
const dbName = 'paperline'

mongo.connect(url, (err, client) => 
{  if (err) 
    {console.error(err)   
        return }  
    console.log('Connected successfully to server')  
    const db = client.db("paperline")
    const collection = db.collection('tweet')
    db.collection.copyTo("tweet_no_duplicate")
})
