import { createClient } from '@supabase/supabase-js'
import fs from 'fs';
import { getSummaryOpenAi } from './openaiCon.js';
const envJson = fs.readFileSync('./env.json', 'utf8');
const env = JSON.parse(envJson);

// Create a single supabase client for interacting with your database
const supabase = createClient(`${env.db_url}`, `${env.api_key}`) 

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function deleteOldData(eventID)
{
    const {data, error} = await supabase.from('fetchdata')
                                        .select('*')
                                        .eq('event_id', eventID)
    if(!error)
    {
        const maxFeches = 30;
        const amountDelete = 3; //for testing
        const amountFetches = data.length;
        
        if(amountFetches>=maxFeches)
        {
            console.log('to many fetches were registered. old data will be deleted')
            console.log(`${amountDelete} rows where deleted all with ids less than ${data[amountDelete-1].id}`)
            await supabase.from('fetchdata')
                            .delete()
                            .lte('id', data[amountDelete-1].id)
        }else
        {
            console.log(`no events were deleted the event with id=${eventID}`)
        }
    }else
    {
        console.error("there was in error while fetching the data to delete the old data",error)
    }
}

async function insertDataToWebsitesTable(title, link,category, imgUrl, source, location)
{
    //add some kind of validation to make sure website doesnt exist
    //fetch all entities of websites; loop through them, if not exist insert
    let eventExist = false;
    const {data, error} = await supabase.from('events')
                                        .select('*')
    for(let i = 0; i<data.length; i++)
    {
        if(data[i].title === title 
            &&data[i].source == source
            &&data[i].location == location
            && data[i].link === link 
            && data[i].category === category)
        {
            eventExist = true;
            break;
        }
    }

    console.log(`the event ${title} exist: ${eventExist}`)
    if(!eventExist)
    {
        //make api call
        console.log(link)
        const description = await getSummaryOpenAi(link);
        console.log(description)
        
        
        const {error: insertError } = await supabase.from('events').insert(
            {
                title: `${title}`,
                link: `${link}`,
                category: `${category}`,
                img_url: `${imgUrl}`,
                source: `${source}`,
                location: `${location}`,
                description: `${description}`

            }
        )
        if(insertError)
        {
            console.error("there was an error while inserting the data: ", insertError)
        }
    }
}
async function insertDataToFetchDataTable(price, date, scrapedAt, eventId, time)
{
    const {error} = await supabase.from("fetchdata").insert(
        {
            price: `${price}`,
            date: `${date}`,
            scraped_at: `${scrapedAt}`,
            event_id: `${eventId}`,
            time: `${time}`
        }
    )
}
async function insertDataFromScraperToDB(title, link, category, source, location, imgUrl,
                                         price, date, scrapedAt, time)
{   
    insertDataToWebsitesTable(title, link, category,imgUrl,source,location)
    await sleep(20000)
    insertDataToWebsitesTable(title, link, category,imgUrl,source,location)
    //ich brauche hier irgendwie die websiteID: idee-fetchall check if entity is object getID
    let eventId = 0;
    const {data, error} = await supabase.from('events').select('*');
    if(!error)
    {
        for(let i = 0; i<data.length;i++)
        {
            if(data[i].title=== title)//hier nur noch title abgleichen, da alle titles unique sein sollten durch vorherige function
            {
                while(eventId ===0)
                {
                    eventId = data[i].id//michel sagt hier muss comment
                }
                break
            }
        }
    }
    await sleep(2000)
    console.log(`id: ${eventId}`)
    insertDataToFetchDataTable(price, date,scrapedAt,eventId,time)
}
async function fetchLatestDataWebsite(eventID)
{
    const {data , error1st} = await supabase
                            .from('fetchdata')
                            .select('id')
                            .eq('event_id', eventID)//like WHERE websiteID= variable websiteID (only works on direct columns of that table)
    
    if (error1st)
    {
        console.error("error: ", error1st)
    }
    if(data.length>0)
    {
        let latestFetchID = 0;
        while(latestFetchID === 0)
        {
            latestFetchID =  data[data.length-1].id //potential bug issue but im assuming that the highest id
                                                    // is always at the end of the returned array
        }

        //second fetch to get the final result with the latest website fetch informatin
        const {data: result , error: error2nd} = await supabase
                                .from('events')
                                .select('*, fetchdata(*)')
                                .eq('id', eventID)
                                .filter('fetchdata.id', 'eq', latestFetchID);//the result has to be data and error
        if (error2nd)
        {
            console.error("error acured while fetching result: ", error2nd)
        }
        else
        {
            console.log("fetched the result successfully")
        }
        let output = result[0] //defining output to the first element since the array will always contain only one element
        //console.log(output.fetchdata[0].date)//example how to access the fetchdata object
                                            //want to get rid of accessing the first index of fetchdata but idk how
        return output;
    }
    return "invalid data, maybe datafetch is empty"
}
async function fetchAllDataDb()
{

    let arr = []
    const {data, error} = await supabase.from('events')
                                        .select('*, fetchdata(*)')
                                        
    if(!error)
    {
        const amountEvents = data.length;
        for(let i = 0; i< amountEvents;i++)
        {
            let mostRecentData = await fetchLatestDataWebsite(data[i].id);
            await deleteOldData(data[i].id)
            arr.push(mostRecentData) 
        }
        //clear not neccessary data
    }else
    {
        console.error(error)
    }
    return arr;
}
export {fetchLatestDataWebsite, insertDataFromScraperToDB, fetchAllDataDb}
//testing functions
//insertDataFromScraperToDB("newTest", "https:newnewnew.com", "test", "testing.com", "Hamburgo", "img.url", "0$", "13.02.2025", "12.02.1025-10.52", "11 00")

//fetchLatestDataWebsite(3)
//deleteOldData(3)
//fetchAllDataDb();