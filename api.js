const dbCon = require('./supabaseCon.js');
const express = require('express')
const app = express()
const port = 3000

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
        res.status(404).statusMessage('you need to provide an id')
    }
    try
    {
        const data = await dbCon.fetchLatestDataWebsite(id)
        console.log(data);
        res.send(data)
    }catch(error)
    {
        res.status(500).statusMessage('something went wrong')
        console.error(error)
    }
})
app.post('pushData', (req, res)=>{

})