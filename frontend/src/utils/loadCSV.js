import fs from 'fs';
import csvParser from 'csv-parser';

export async function loadCSV(filePath) {
    const rows = [];
  
    return new Promise((resolve, reject) => {
      fs.createReadStream(filePath)
        .pipe(csvParser())
        .on('data', (row) => {
          rows.push(row);
        })
        .on('end', () => {
          resolve(rows);
        })
        .on('error', (error) => {
          reject(error);
        });
    });
  }