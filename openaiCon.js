import fs from 'fs'
const envJSON = fs.readFileSync('./env.json','utf8')
const env = JSON.parse(envJSON)
import axios from 'axios';
import OpenAI from "openai";
import { encode, decode } from 'gpt-3-encoder';
const openai = new OpenAI({
    apiKey: env.openai_api_key,
});
const testurl = "https://vernetztgegenrechts.hamburg/event/fuehrung-und-gespraech-in-der-gedenkstaette-fuhlsbuettel-2/2025-03-16/"
//limit max tokens per request to ensure the request isnt to expensive
function truncateText(text, maxTokens) {
    const encoded = encode(text);
    if (encoded.length > maxTokens) {
        const truncated = encoded.slice(0, maxTokens);
        return truncated.map(token => decode([token])).join('');
    }
    return text;
}
//receive html data of specific website
async function fetchWebsiteText(url)
{
    try
    {
        const response = await axios.get(url);
        if(response)
        {
            let html = response.data;

            // Remove script and style tags
            html = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
            html = html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');

            // Remove class names
            html = html.replace(/\sclass="[^"]*"/gi, '');

            // Remove specific elements (footer, nav)
            html = html.replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, '');
            html = html.replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, '');

            // Extract text content
            html = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
            return truncateText(html,300);
        }
        
    }
    catch(error)
    {
        console.error('error while fetching the website content', error)
        return null;
    }
}
//call openai api and get request of parsed html data of url provided as an argument
async function getSummaryOpenAi(url)
{
    const data = await fetchWebsiteText(url);
    if(data)
    {
        const summary = await openai.chat.completions.create({
            model:"gpt-4-turbo",
            messages: [
                {
                    role: "system", content: "you are a assistant" 
                },
                {
                    role: "user",
                    content: `summarizes the html content provided.
                                    just use info describing the event and 
                                    not e.g. the date, location or tickets etc. 
                                    we will inform the user in another way
                                    ${data}
                                    only output 2 to 3 sentences`,
                },
            ],
            max_tokens: 100,
            store: false,
        })
        //console.log(summary.choices[0].message.content)
        return summary.choices[0].message.content
    }
    else
    {
        console.error('error while providing the html data');
    }
    
}

export {getSummaryOpenAi}
//fetchWebsiteText(testurl)
//getSummaryOpenAi(testurl)
