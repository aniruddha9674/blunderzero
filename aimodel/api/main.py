from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from train import MoveManager

app = FastAPI()

class MoveRequest(BaseModel):
    fen: str
    elo: int

@app.post("/move")
def best_move(req: MoveRequest):
    try:
        print(f"Incoming FEN: {req.fen}")
        print(f"Incoming ELO: {req.elo}")

        move_manager = MoveManager(req.elo)
        result = move_manager.get_trained_move(req.fen)

        print(f"Returning move: {result['move']}")
        return {
            "best_move": result["move"],
            "evaluation": result["evaluation"]
        }
    except Exception as e:
        print(f"Error in /move: {e}")
        raise HTTPException(status_code=500, detail=str(e))
