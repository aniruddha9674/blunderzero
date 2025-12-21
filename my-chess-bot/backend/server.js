import express from 'express';
import path from 'path';
import axios from 'axios';
import cors from 'cors';
const app = express();
const PORT = process.env.PORT || 8000;

app.use(express.static(path.join('../', 'dist')));
app.use(express.json());
app.use(cors());
app.post('/move', async (req, res) => {
  try {
    const { fen, elo } = req.body;
    console.log("Node server received:", fen, elo); // ADD THIS

    const response = await axios.post('http://127.0.0.1:8000/move', { fen, elo });

    const { best_move, evaluation } = response.data;
    res.json({ move: best_move, evaluation });
  } catch (error) {
    console.error('Error getting move from FastAPI:', error.message);
    console.error('Error details:', error.response ? error.response.data : 'No response data');
    res.status(500).send('Error getting move from AI');
  }
});


app.get('/', (req, res) => {
  res.sendFile(path.join('../', 'dist', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
