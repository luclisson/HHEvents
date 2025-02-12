import { createClient } from '@supabase/supabase-js'
import fs from 'fs';
const envJson = fs.readFileSync('./env.json', 'utf8');
const env = JSON.parse(envJson);

// Create a single supabase client for interacting with your database
const supabase = createClient(`${env.db_url}`, `${env.api_key}`) 


async function insertDataToWebsitesTable(title, link, description, category)
{
    //add some kind of validation to make sure website doesnt exist
    //fetch all entities of websites; loop through them, if not exist insert
    let eventExist = false;
    const {data, error} = await supabase.from('websites')
                                        .select('*')
    for(let i = 0; i<data.length; i++)
    {
        if(data[i].title === title 
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
        const {error: insertError } = await supabase.from('websites').insert(
            {
                title: `${title}`,
                link: `${link}`,
                description: `${description}`,
                category: `${category}`,
            }
        )
        if(insertError)
        {
            console.error("there was an error while inserting the data: ", insertError)
        }
    }
}

async function insertDataToFetchDataTable(price, date, duration, websiteID)
{
    const {error} = await supabase.from("fetchdata").insert(
        {
            price: `${price}`,
            date: `${date}`,
            duration: `${duration}`,
            websiteid: `${websiteID}`
        }
    )
}
async function insertDataFromScraperToDB(title, link, description, category,
                                         price, date, duration)
{   
    insertDataToWebsitesTable(title,link,description,category)
    //ich brauche hier irgendwie die websiteID: idee-fetchall check if entity is object getID
    let eventID = 0;
    const {data, error} = await supabase.from('websites').select('*');
    if(!error)
    {
        for(let i = 0; i<data.length;i++)
        {
            if(data[i].title=== title)//hier nur noch title abgleichen, da alle titles unique sein sollten durch vorherige function
            {
                eventID = data[i].id
                break
            }
        }
    }
    console.log(`website id of ${title} is ${eventID}`)
    insertDataToFetchDataTable(price, date, duration, eventID)
}
async function fetchLatestDataWebsite(websiteID)
{
    const {data , error1st} = await supabase
                            .from('fetchdata')
                            .select('id')
                            .eq('websiteid', websiteID)//like WHERE websiteID= variable websiteID (only works on direct columns of that table)
    
    if (error1st)
    {
        console.error("error: ", error1st)
    }
    let latestFetchID =  data[data.length-1].id //potential bug issue but im assuming that the highest id
                                                // is always at the end of the returned array

    //second fetch to get the final result with the latest website fetch informatin
    const {data: result , error: error2nd} = await supabase
                            .from('websites')
                            .select('*, fetchdata(*)')
                            .eq('id', websiteID)
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
    console.log(output)
    console.log(output.fetchdata[0].date)//example how to access the fetchdata object
                                        //want to get rid of accessing the first index of fetchdata but idk how
}


//testing functions
//insertDataFromScraperToDB("testFromJS","https:google.com","just a test from the ide","test","6","23.05.2005",5)
//fetchLatestDataWebsite(3)



//todos: 
/*
if anount fetches per website is 60 delete all except one
define test data until scraper py file is ready
*/