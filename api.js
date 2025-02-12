const dbCon = require('./supabaseCon.js');
const cron = require('node-cron')
const express = require('express')
const app = express()
const port = 3000

app.use(express.json())

app.get('/', (req, res) => {
    res.send('application is running')//every route has a request and a response var 
})
app.listen(port, () => {
    console.log(`api is running at port ${port}`)
})

app.get('/fetch/:id', async (req, res) => {
    const id = req.params.id
    if(!id)
    {
        res.status(404).statusMessage('you need to provide an id')
    }
    try
    {
        const data = await dbCon.fetchLatestDataWebsite(id)//test data
        console.log(data);
        res.send(data)
    }catch(error)
    {
        res.status(500).statusMessage('something went wrong')
        console.error(error)
    }
})
app.get('/fetchData', async (req, res)=>{
    console.log("fetchData route was called")
    try
    {
        //implement fetching db body
        const data = await dbCon.fetchAllDataDb();
        res.send(data);
    }catch(error)
    {
        res.status(500).statusMessage('something went wrong')
    }
})

cron.schedule('30 01 * * *', async ()=>{
    //fetches db everyday at 1.30am
    const response = await fetch('http://localhost:3000/fetchData',{
        method: 'GET'
    });
    const data = await response.json();//not sure if needed. right now it works but i think this could cause errors
    console.log(data) 
})