import os
from stockfish import Stockfish
import chess

# Absolute path to Stockfish binary
STOCKFISH_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "engines", "stockfish", "stockfish-windows-x86-64-avx2.exe")
)

# Optional: check if Stockfish exists
if not os.path.exists(STOCKFISH_PATH):
    raise FileNotFoundError(f"Stockfish not found at: {STOCKFISH_PATH}")

class StockfishHandler:
    """Handles Stockfish engine initialization and communication."""
    def __init__(self, path=STOCKFISH_PATH):
        self.stockfish = Stockfish(path=path)

    def get_best_move(self, fen, depth=20):
        """Gets the best move based on a given FEN position."""
        self.stockfish.set_fen_position(fen)
        self.stockfish.set_depth(depth)
        return self.stockfish.get_best_move()

    def get_eval_score(self, fen):
        """Gets the evaluation score based on a given FEN position."""
        self.stockfish.set_fen_position(fen)
        return self.stockfish.get_evaluation()

class ScholarsMate:
    """Handles Scholar's Mate sequence logic for Black (bot)."""
    def __init__(self):
        # Black's replies in response to common blunder sequence
        self.scholars_mate_black_moves = [
            "e7e5",  # respond to e2e4
            "d8h4",  # if f2f3 is played
            "h4h3"   # deliver mate if g2g3 is played
        ]

    def check_scholars_mate(self, board):
        """Returns next move in Black's Scholar’s Mate sequence, if applicable."""
        history = [move.uci() for move in board.move_stack]

        # Create a filtered list of only Black's past moves
        black_moves_so_far = history[1::2]  # Black moves only

        matched = 0
        for i, move in enumerate(black_moves_so_far):
            if i < len(self.scholars_mate_black_moves) and move == self.scholars_mate_black_moves[i]:
                matched += 1
            else:
                break

        if matched < len(self.scholars_mate_black_moves):
            return self.scholars_mate_black_moves[matched]
        return None


class MoveManager:
    """Manages the logic for generating the best move."""
    def __init__(self, elo):
        self.elo = elo
        self.stockfish_handler = StockfishHandler()
        self.scholars_mate = ScholarsMate()

    def get_trained_move(self, fen: str) -> dict:
        board = chess.Board(fen)
        
        # If Elo is low, try Scholar's Mate logic
        if self.elo < 200:
            print("ELO is low, attempting Scholar's Mate sequence...")
            next_scholar_move = self.scholars_mate.check_scholars_mate(board)
            if next_scholar_move:
                move = chess.Move.from_uci(next_scholar_move)
                if move in board.legal_moves:
                    print(f"Executing Scholar's Mate move: {next_scholar_move}")
                    return {
                        "move": move.uci(),
                        "evaluation": {"type": "custom", "value": "Scholar’s Mate Attempt"}
                    }
                else:
                    print(f"Move {next_scholar_move} is not legal. Scholar's Mate cannot be played.")
            else:
                print("Scholar's Mate sequence complete or blocked. Proceeding with Stockfish.")

        # Default to Stockfish if Scholar's Mate fails or Elo >= 200
        print("ELO is sufficient or Scholar's Mate is blocked. Using Stockfish for best move.")
        try:
            best_move = self.stockfish_handler.get_best_move(fen, depth=16)
            evaluation = self.stockfish_handler.get_eval_score(fen)
            print(f"Stockfish recommended move: {best_move}")
            return {
                "move": best_move,
                "evaluation": evaluation
            }
        except Exception as e:
            print(f"Error occurred while fetching best move from Stockfish: {e}")
            return {
                "move": None,
                "evaluation": {"type": "error", "value": "Error fetching best move from Stockfish"}
            }

