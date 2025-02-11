import { createClient } from '@supabase/supabase-js'
import fs from 'fs';
const envJson = fs.readFileSync('./env.json', 'utf8');
const env = JSON.parse(envJson);

// Create a single supabase client for interacting with your database
const supabase = createClient(`${env.db_url}`, `${env.api_key}`) 


async function insertDataToWebsitesTable(title, link, description, category, idFetch)
{
    const { error } = await supabase.from('websites').insert(
        {
            title: `${title}`,
            link: `${link}`,
            description: `${description}`,
            category: `${category}`,
            idFetch: `${idFetch}`
            // for me it looks like i could have a problem with adding multiple idFetch to one website
        }
    )
}
//fetching data
const { data, error } = await supabase
  .from('websites')
  .select('*, fetchdata(*)'); 
 
//printing data and some column from fetch data table
console.log(data);
let amountWebsites = data.length;
for(let i = 0; i<amountWebsites;i++)
{
    console.log(data[i].fetchdata.date)
}