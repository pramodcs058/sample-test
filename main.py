from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape

from tic_tac_toe import TicTacToeGame

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

game = TicTacToeGame()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    html = templates.get_template("index.html").render(
        request=request,
        game=game,
        board=list(enumerate(game.board)),
    )
    return HTMLResponse(html)

@app.post("/start")
def start_game(
    x_player: str = Form("Player X"),
    o_player: str = Form("Player O"),
):
    game.start(x_player.strip() or "Player X", o_player.strip() or "Player O")
    return RedirectResponse("/", status_code=303)

@app.post("/move")
def make_move(index: int = Form(...)):
    game.make_move(index)
    return RedirectResponse("/", status_code=303)

@app.post("/reset")
def reset_board(reset_type: str = Form("round")):
    if reset_type == "scores":
        game.reset_scores()
    else:
        game.reset_round()
    return RedirectResponse("/", status_code=303)
