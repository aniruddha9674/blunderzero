import chess.pgn
import os

def load_trap_games(pgn_folder):
    games = []
    
    for filename in os.listdir(pgn_folder):
        if filename.endswith('.pgn'):
            path = os.path.join(pgn_folder, filename)
            with open(path, encoding="utf-8") as pgn_file:
                while True:
                    game = chess.pgn.read_game(pgn_file)
                    if game is None:
                        break
                    games.append(game)
    
    return games
