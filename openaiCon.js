import fs from 'fs'
const envJSON = fs.readFileSync('./env.json','utf8')
const env = JSON.parse(envJSON)
import OpenAI from "openai";
const openai = new OpenAI({
    apiKey: env.openai_api_key,
});

const summary = await openai.chat.completions.create({
    model:"gpt-4-turbo",
    messages: [
        {
            role: "system", content: "you are a assistant" 
        },
        {
            role: "user",
            content: "summarizes the content provided",
        },
    ],
    max_tokens: 100,
    store: false,
})

console.log(summary.choices[0].message.content)