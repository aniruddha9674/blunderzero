import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// Convert ES module URL to __dirname (works in ESM)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ✅ Full path to Stockfish binary (make sure this matches the exact file name)
const stockfishPath = path.join(__dirname, 'stockfish', 'stockfish-windows-x86-64-avx2.exe'); // Use .exe for Windows

// ✅ Get best move from Stockfish given a FEN
export const getStockfishMove = (fen) => {
  return new Promise((resolve, reject) => {
    const stockfish = spawn(stockfishPath);

    let output = '';

    stockfish.stdout.on('data', (data) => {
      const text = data.toString();
      output += text;

      // Extract bestmove using regex
      const match = text.match(/bestmove\s+(\w{4,5})/);
      if (match) {
        resolve(match[1]);
        stockfish.kill(); // Clean up process
      }
    });

    stockfish.stderr.on('data', (data) => {
      console.error('Stockfish error:', data.toString());
      reject(new Error(data.toString()));
    });

    stockfish.on('error', (err) => {
      console.error('Failed to start Stockfish:', err);
      reject(err);
    });

    stockfish.on('close', (code) => {
      if (code !== 0 && !output.includes('bestmove')) {
        reject(new Error(`Stockfish exited with code ${code}`));
      }
    });

    // Send commands to Stockfish engine
    stockfish.stdin.write(`uci\n`); // Optional: helps with debugging
    stockfish.stdin.write(`isready\n`);
    stockfish.stdin.write(`position fen ${fen}\n`);
    stockfish.stdin.write(`go movetime 1500\n`);
  });
};
