import { fetchLatestDataWebsite, insertDataFromScraperToDB, fetchAllDataDb } from './supabaseCon.js';
import { loadJSON } from './scraperCon.js';
import cron from 'node-cron';
import express from 'express';


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
        res.status(404).send('you need to provide an id')
    }
    try
    {
        const data = await fetchLatestDataWebsite(id)//test data
        console.log(data);
        res.send(data)
    }catch(error)
    {
        res.status(500).send('something went wrong')
        console.error(error)
    }
})
app.get('/insertData', async (req, res) =>{
    const data = loadJSON('test.json');
    console.log(data)
    for(let i = 0; i< data.length; i++)
    {
        /*
        wird noch gebraucht um die geupdate struktur zu testen
        console.log(`title: ${data[i].title}`)
        console.log(`link: ${data[i].link}`)
        console.log(`category ${data[i].event_type}`)
        console.log(`source ${data[i].source}`)
        console.log(`img url: ${data[i].img_url}`)
        console.log(`price: ${data[i].price}`)
        console.log(`date: ${data[i].event_date}`)
        console.log(`scraped at: ${data[i].scraped_at}`)
        */
        insertDataFromScraperToDB(data[i].title, data[i].link,
            data[i].event_type, data[i].source, 'hamburg', data[i].img_url, 
            data[i].price, data[i].event_date, data[i].scraped_at, "13 00");
    }
    if(!data)
    {
        res.status(500).send('error while getting scraper data')
    }else
    {
        res.send('successfully received data from the scraper and inserted it to the db')
    }
})
app.get('/fetchData', async (req, res)=>{
    console.log("fetchData route was called")
    try
    {
        const data = await fetchAllDataDb();
        res.send(data);
    }catch(error)
    {
        res.status(500).send('something went wrong')
    }
})

cron.schedule('45 10 * * *', async ()=>{
    //fetches db everyday at 1.30am
    const response = await fetch('http://localhost:3000/fetchData',{
        method: 'GET'
    });
    const data = await response.json();//not sure if needed. right now it works but i think this could cause errors
})

cron.schedule('37 15 * * *', async ()=>{
    //code to insert test data, later scraper data
    const response = await fetch('http://localhost:3000/insertData',{
        method: 'GET'
    });
    console.log(response)
})


/*
todos:
- use data from db and update frontend
*/