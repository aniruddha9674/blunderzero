import { useState } from 'react';
import ChessBoard from './ChessBoard';
import React from 'react';

function App() {
  const [elo, setElo] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    if (elo >= 100 && elo <= 3000) {
      setSubmitted(true);
    } else {
      alert("Please enter a valid ELO between 100 and 3000");
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      {!submitted ? (
        <>
          <h1>Enter Your ELO</h1>
          <input 
            type="number"
            value={elo}
            onChange={(e) => setElo(e.target.value)}
            placeholder="E.g. 850"
            style={{ padding: '0.5rem', fontSize: '1rem' }}
          />
          <br /><br />
          <button onClick={handleSubmit}>Start Game</button>
        </>
      ) : (
        <ChessBoard elo={parseInt(elo)} />
      )}
    </div>
  );
}

export default App;
