const { spawn } = require('child_process');
const { writeFileSync, unlinkSync } = require('fs');
const path = require('path');

exports.handler = async (event, context) => {
  return new Promise((resolve, reject) => {
    // Write event data to temporary files
    const eventFile = path.join(__dirname, 'temp_event.json');
    const contextFile = path.join(__dirname, 'temp_context.json');
    
    try {
      writeFileSync(eventFile, JSON.stringify(event));
      writeFileSync(contextFile, JSON.stringify(context));
    } catch (e) {
      resolve({
        statusCode: 500,
        body: `Failed to write temp files: ${e.message}`
      });
      return;
    }

    // Create a Python script that handles the WSGI request
    const pythonScript = `
import sys
import os
import json
sys.path.insert(0, '${path.join(__dirname, '../..').replace(/\\/g, '\\\\')}')

from app import app
import serverless_wsgi

with open('${eventFile.replace(/\\/g, '\\\\')}', 'r') as f:
    event = json.load(f)
with open('${contextFile.replace(/\\/g, '\\\\')}', 'r') as f:
    context = json.load(f)

try:
    response = serverless_wsgi.handle_request(app, event, context)
    print("RESPONSE_START")
    print(json.dumps(response))
    print("RESPONSE_END")
except Exception as e:
    print("ERROR_START")
    print(json.dumps({"statusCode": 500, "body": str(e)}))
    print("ERROR_END")
`;

    const python = spawn('poetry', ['run', 'python', '-c', pythonScript], {
      cwd: path.join(__dirname, '../..'),
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    python.on('close', (code) => {
      // Cleanup temp files
      try {
        unlinkSync(eventFile);
        unlinkSync(contextFile);
      } catch (e) {
        // Ignore cleanup errors
      }

      try {
        // Extract the JSON response
        const responseStart = stdout.indexOf('RESPONSE_START');
        const responseEnd = stdout.indexOf('RESPONSE_END');
        const errorStart = stdout.indexOf('ERROR_START');
        
        if (responseStart !== -1 && responseEnd !== -1) {
          const responseJson = stdout.substring(responseStart + 14, responseEnd).trim();
          const response = JSON.parse(responseJson);
          resolve(response);
        } else if (errorStart !== -1) {
          const errorEnd = stdout.indexOf('ERROR_END');
          const errorJson = stdout.substring(errorStart + 11, errorEnd).trim();
          const error = JSON.parse(errorJson);
          resolve(error);
        } else {
          resolve({
            statusCode: 500,
            body: `Python execution failed. Code: ${code}, Stdout: ${stdout}, Stderr: ${stderr}`
          });
        }
      } catch (parseError) {
        resolve({
          statusCode: 500,
          body: `Failed to parse response: ${parseError.message}. Output: ${stdout}`
        });
      }
    });

    python.on('error', (error) => {
      resolve({
        statusCode: 500,
        body: `Failed to start Python: ${error.message}`
      });
    });
  });
};