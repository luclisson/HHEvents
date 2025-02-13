import { fetchLatestDataWebsite, insertDataFromScraperToDB, fetchAllDataDb } from './supabaseCon.js';
import { loadJSON } from './scraperCon.js';
import cron from 'node-cron';
import express from 'express';
import cors from 'cors';


const app = express()
const port = 3000

app.use(cors())
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
    const data = loadJSON('all_events.json');
    for(let i = 0; i< 5; i++) //5 to not fetch 2000 entities
    {
        /*
        //wird noch gebraucht um die geupdate struktur zu testen
        console.log(`title: ${data[i].title}`)
        console.log(`link: ${data[i].link}`)
        console.log(`category ${data[i].category}`)
        console.log(`source ${data[i].source_url}`)
        console.log(`img url: ${data[i].img_url}`)
        console.log(`price: ${data[i].price}`)
        console.log(`date: ${data[i].event_date}`)
        console.log(`scraped at: ${data[i].scraped_at}`)
        console.log(`locaiton: ${data[i].location}`)
        console.log(`time: ${data[i].time}`)
        */
        
        insertDataFromScraperToDB(data[i].title, data[i].link,
            data[i].category, data[i].source_url, data[i].location, data[i].img_url, 
            data[i].price, data[i].event_date, data[i].scraped_at, data[i].time);
            
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

cron.schedule('15 19 * * *', async ()=>{
    //fetches db everyday at 1.30am
    const response = await fetch('http://localhost:3000/fetchData',{
        method: 'GET'
    });
    const data = await response.json();//not sure if needed. right now it works but i think this could cause errors
})

cron.schedule('14 19 * * *', async ()=>{
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