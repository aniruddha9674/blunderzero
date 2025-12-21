from stockfish import Stockfish
import os

# Absolute path to Stockfish binary
STOCKFISH_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "engines","stockfish", "stockfish-windows-x86-64-avx2.exe")
)

# Optional: check if it exists
if not os.path.exists(STOCKFISH_PATH):
    raise FileNotFoundError(f"Stockfish not found at: {STOCKFISH_PATH}")

# Initialize engine
stockfish = Stockfish(path=STOCKFISH_PATH)
def get_best_move(fen, depth=20):  # Increase depth to 20 or more
    stockfish.set_fen_position(fen)
    stockfish.set_depth(depth)
    return stockfish.get_best_move()

def get_eval_score(fen):
    stockfish.set_fen_position(fen)
    return stockfish.get_evaluation()
