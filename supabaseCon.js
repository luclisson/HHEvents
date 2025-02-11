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
  .from('websites')
  .select('*'); 
 
//printing data and some column from fetch data table
console.log(data);
let amountWebsites = data.length;
for(let i = 0; i<amountWebsites;i++)
{
    console.log(data[i])
}