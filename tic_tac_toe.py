from dataclasses import dataclass, field
from typing import Dict, List, Optional

WINNING_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


@dataclass
class TicTacToeGame:
    players: Dict[str, str] = field(default_factory=lambda: {"X": "Player X", "O": "Player O"})
    scores: Dict[str, int] = field(default_factory=lambda: {"X": 0, "O": 0})
    current_player: str = "X"
    board: List[str] = field(default_factory=lambda: [""] * 9)
    game_active: bool = False
    status: str = "Enter both names and start the game."

    def start(self, x_name: str, o_name: str) -> None:
        x_name = x_name.strip() or "Player X"
        o_name = o_name.strip() or "Player O"

        if x_name == o_name:
            self.status = "Please use two different player names."
            self.game_active = False
            return

        same_players = self.players["X"] == x_name and self.players["O"] == o_name
        self.players = {"X": x_name, "O": o_name}
        if not same_players:
            self.scores = {"X": 0, "O": 0}

        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        self.status = f"{self.players[self.current_player]}'s turn ({self.current_player})."

    def make_move(self, index: int) -> None:
        if not self.game_active or index < 0 or index >= 9:
            return

        if self.board[index]:
            return

        self.board[index] = self.current_player
        winner = self._check_winner()

        if winner:
            self.scores[winner] += 1
            self.game_active = False
            self.status = f"{self.players[winner]} wins! ({winner})"
            return

        if all(self.board):
            self.game_active = False
            self.status = "It’s a draw. Start a new round."
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.status = f"{self.players[self.current_player]}'s turn ({self.current_player})."

    def _check_winner(self) -> Optional[str]:
        for a, b, c in WINNING_LINES:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def reset_round(self) -> None:
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        self.status = f"{self.players[self.current_player]}'s turn ({self.current_player})."

    def reset_scores(self) -> None:
        self.scores = {"X": 0, "O": 0}
        self.status = "Scores reset. Continue playing."
