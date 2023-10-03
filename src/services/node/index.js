import { readFileSync } from 'node:fs';
import 'node:os' // For some reason, this import is required to resolve WebSocketServer
import { WebSocketServer } from 'ws';
import { createServer } from 'node:https';

const cfg = {
  ssl: false,
  port: process.env.PORT || 3000,
  ssl_key: './ssl.key',
  ssl_cert: './ssl.crt'
};

const port = process.env.PORT || 3000

const server = cfg.ssl ? createServer({
  cert: readFileSync('/path/to/cert.pem'),
  key: readFileSync('/path/to/key.pem')
}) : null;

const wss = server ? new WebSocketServer({ server }).listen(cfg.port) : new WebSocketServer({ port: cfg.port });

wss.on('connection', function connection(ws) {

  ws.on('error', console.error);
  ws.on('message', (message) => {
    const { id, command, payload } = JSON.parse(message)
    
    const response = { id, command, response: true }
    if (command === 'platform') response.payload = process.platform
    
    else {
      response.error = `Unknown command: ${command}`
      delete response.payload
    }

    ws.send(JSON.stringify(response))

  });
});

console.log(`Server running at http://localhost:${port}/`)
