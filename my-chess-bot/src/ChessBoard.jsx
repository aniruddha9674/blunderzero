import { useState, useEffect } from 'react';
import { Chess } from 'chess.js';
import { Chessboard } from 'react-chessboard';
import React from 'react';

const game = new Chess();

function ChessBoard({ elo }) {
  const [fen, setFen] = useState(game.fen());

  useEffect(() => {
    console.log("User ELO:", elo); // ✅ Debug
  }, [elo]);

  // ✅ Get the bot's move from the backend with FEN and ELO
  const getBotMove = async (fen, elo) => {
    try {
      const response = await fetch('http://localhost:8000/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fen, elo }),
      });

      const data = await response.json();

      const moveStr = data.move || data.best_move; // ✅ Support both keys

      return moveStr; // UCI string like "e2e4"
    } catch (err) {
      console.error("Error getting bot move:", err);
      return null;
    }
  };

  // ✅ Handle player's move, then let the bot respond
  const handlePlayerMove = async (sourceSquare, targetSquare) => {
    const move = game.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q',
    });

    if (move === null) return false;

    setFen(game.fen());
    console.log("Player Move:", move);

    const updatedFEN = game.fen();
    const botMove = await getBotMove(updatedFEN, elo); // ✅ PASS elo!

    if (!botMove) return true;

    console.log("Bot Move:", botMove);

    game.move({
      from: botMove.substring(0, 2),
      to: botMove.substring(2, 4),
      promotion: 'q',
    });

    setFen(game.fen());
    return true;
  };

  return (
    <div style={{ maxWidth: "500px", margin: "auto" }}>
      <h2>Chess Game</h2>
      <Chessboard position={fen} onPieceDrop={handlePlayerMove} />
    </div>
  );
}

export default ChessBoard;
