import { createClient } from '@supabase/supabase-js'
import fs from 'fs';
const envJson = fs.readFileSync('./env.json', 'utf8');
const env = JSON.parse(envJson);

// Create a single supabase client for interacting with your database
const supabase = createClient(`${env.db_url}`, `${env.api_key}`) 


async function insertDataToWebsitesTable(title, link, description, category)
{
    const { error } = await supabase.from('websites').insert(
        {
            title: `${title}`,
            link: `${link}`,
            description: `${description}`,
            category: `${category}`,
        }
    )
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
//insertDataToWebsitesTable("testFromJS", "https:google.com", "just a test from the ide", "test")
//insertDataToFetchDataTable("5",'22.02.2222',1, 3)

//fetching data
const { data, error } = await supabase
  .from('fetchdata')
  .select('*');
  //need a join which fetches the website and the newest fetchData where websiteID=id

 
//printing data and some column from fetch data table
/*
console.log(data);
let amountWebsites = data.length;
for(let i = 0; i<amountWebsites;i++)
{
    console.log(data[i])
}
*/
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
    console.log(result)
}
fetchLatestDataWebsite(3)
//todos: 
/*
check if event title already exists if not --> insert
fetches in db
if anount fetches per website is 60 delete all except one
define test data until scraper py file is ready
*/