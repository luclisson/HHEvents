const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
    res.send('application is running')
})
app.listen(port, () => {
    console.log(`api is running at port ${port}`)
})