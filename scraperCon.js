import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function loadJSON(filename) {
  let output = "";
  try {
    const filePath = path.join(__dirname, filename); // Get absolute path
    const data = fs.readFileSync(filePath, 'utf8'); // Read file synchronously
    const jsonData = JSON.parse(data); // Parse JSON
    output = jsonData;
  } catch (error) {
    console.error('Error loading JSON:', error);
  }
  return output;
}

export { loadJSON };