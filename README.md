# sample-test

A browser-based Tic Tac Toe game built with FastAPI.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the web app:

```bash
uvicorn main:app --reload
```

Open the app in your browser:

```text
http://127.0.0.1:8000/
```

Enter names for both players, click "Start / Restart Game", then click the board cells to play. The session scoreboard tracks wins for each player.

## Files

- `main.py` — FastAPI server and request handlers
- `tic_tac_toe.py` — shared game logic and score tracking
- `templates/index.html` — browser UI template
- `static/style.css` — page styling
>
> If you are running in a headless container environment, the app now falls back to the Qt `offscreen` platform so it can initialize without a display server.
