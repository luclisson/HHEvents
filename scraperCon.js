const fs = require('fs');
const path = require('path');

function loadJSON() {
  try {
    const filePath = path.join(__dirname, 'test.json'); // Get absolute path
    const data = fs.readFileSync(filePath, 'utf8'); // Read file synchronously
    const jsonData = JSON.parse(data); // Parse JSON
    console.log(jsonData);
  } catch (error) {
    console.error('Error loading JSON:', error);
  }
}

loadJSON();