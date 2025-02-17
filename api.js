import { fetchLatestDataWebsite, insertDataFromScraperToDB, fetchAllDataDb } from './supabaseCon.js';
import { loadJSON } from './scraperCon.js';
import cron from 'node-cron';
import express from 'express';
import cors from 'cors';
import {exec} from 'child_process';
import { stderr } from 'process';
import fs from 'fs'


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
    for(let i = 0; i< 1; i++) //1 to not fetch 2000 entities and because of api pricing...
    {
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

cron.schedule('15 10 * * *', async ()=>{
    //fetches db everyday at 1.30am
    //used on frontend
    const response = await fetch('http://localhost:3000/fetchData',{
        method: 'GET'
    });
    const data = await response.json();//not sure if needed. right now it works but i think this could cause errors
})

cron.schedule('33 22 * * *', async ()=>{
    //code to insert test data, later scraper data
    const response = await fetch('http://localhost:3000/insertData',{
        method: 'GET'
    });
    console.log(response)
})
cron.schedule('00 10 * * *', async()=>{
    console.log('cron schedule has been called');
    //clear last loaded data to not load it twice
    clearJSONFile('./all_events.json');
    //python script call main.py
    exec('python3 ./scraper/main.py', (error, stdout, stderr)=>{
        if(error)
        {
            console.error(`error executing the script: ${error.message}`);
            return;
        }
        if(stderr)
        {
            console.log(`error while running the script: ${stderr}`);
            return;
        }
        console.log(`script was successfully executed`);
        console.log(`printed: ${stdout}`);
    });
})

function clearJSONFile(filePath) {
    try {
        fs.writeFileSync(filePath, '[]', 'utf8');
        console.log(`Cleared JSON file: ${filePath}`);
    } catch (error) {
        console.error(`Error clearing JSON file: ${error.message}`);
    }
}
