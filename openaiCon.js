import fs from 'fs'
const envJSON = fs.readFileSync('./env.json','utf8')
const env = JSON.parse(envJSON)
import axios from 'axios';
import OpenAI from "openai";
import { encode, decode } from 'gpt-3-encoder';
const openai = new OpenAI({
    apiKey: env.openai_api_key,
});
function truncateText(text, maxTokens) {
    const encoded = encode(text);
    if (encoded.length > maxTokens) {
        const truncated = encoded.slice(0, maxTokens);
        return truncated.map(token => decode([token])).join('');
    }
    return text;
}
const url = "https://docksfreiheit36.de/event?slug=050a0c7a-f093-4ae9-917d-d36c81f6334c&clr=red";
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
            const splitIndex = html.indexOf('</head>') + 7; //removing everything before the body to not include css and script data
            const substring = html.substring(splitIndex);
            console.log(substring)
            const text = truncateText(substring,400)
            return substring;
        }
        
    }
    catch(error)
    {
        console.error('error while fetching the website content', error)
        return null;
    }
}

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
        console.log(summary.choices[0].message.content)
    }
    else
    {
        console.error('error while providing the html data');
    }
    
}
fetchWebsiteText(url)
//getSummaryOpenAi(url)
