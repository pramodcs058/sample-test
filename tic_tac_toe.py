import sys
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(420, 520)

        self.players = {"X": "Player 1", "O": "Player 2"}
        self.scores = {"X": 0, "O": 0}
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = False

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        layout.addWidget(self._build_player_panel())
        layout.addWidget(self._build_score_panel())
        layout.addWidget(self._build_board_panel())
        layout.addLayout(self._build_control_panel())

        self._update_status_label("Enter both names and click Start Game.")

    def _build_player_panel(self):
        group = QGroupBox("Players")
        grid = QGridLayout()
        grid.setSpacing(8)

        grid.addWidget(QLabel("Player X name:"), 0, 0)
        self.player_x_input = QLineEdit()
        self.player_x_input.setPlaceholderText("Enter name for X")
        grid.addWidget(self.player_x_input, 0, 1)

        grid.addWidget(QLabel("Player O name:"), 1, 0)
        self.player_o_input = QLineEdit()
        self.player_o_input.setPlaceholderText("Enter name for O")
        grid.addWidget(self.player_o_input, 1, 1)

        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        grid.addWidget(self.start_button, 2, 0, 1, 2)

        group.setLayout(grid)
        return group

    def _build_score_panel(self):
        group = QGroupBox("Scoreboard")
        grid = QGridLayout()
        grid.setSpacing(8)

        self.score_label_x = QLabel("X: 0")
        self.score_label_o = QLabel("O: 0")
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)

        grid.addWidget(self.score_label_x, 0, 0)
        grid.addWidget(self.score_label_o, 0, 1)
        grid.addWidget(self.status_label, 1, 0, 1, 2)

        group.setLayout(grid)
        return group

    def _build_board_panel(self):
        group = QGroupBox("Board")
        grid = QGridLayout()
        grid.setSpacing(6)

        self.cell_buttons = []
        for index in range(9):
            button = QPushButton("")
            button.setFixedSize(120, 120)
            button.setStyleSheet(
                "font-size: 36px; font-weight: bold; background: #f7f7f7;"
            )
            button.clicked.connect(partial(self.make_move, index))
            self.cell_buttons.append(button)
            row = index // 3
            col = index % 3
            grid.addWidget(button, row, col)

        group.setLayout(grid)
        return group

    def _build_control_panel(self):
        hbox = QHBoxLayout()
        hbox.setSpacing(12)

        self.new_round_button = QPushButton("New Round")
        self.new_round_button.clicked.connect(self.reset_board)
        self.new_round_button.setEnabled(False)

        self.reset_scores_button = QPushButton("Reset Scores")
        self.reset_scores_button.clicked.connect(self.reset_scores)
        self.reset_scores_button.setEnabled(False)

        hbox.addWidget(self.new_round_button)
        hbox.addWidget(self.reset_scores_button)
        return hbox

    def start_game(self):
        x_name = self.player_x_input.text().strip() or "Player X"
        o_name = self.player_o_input.text().strip() or "Player O"

        if x_name == o_name:
            QMessageBox.warning(self, "Name Required", "Please enter two different player names.")
            return

        self.players = {"X": x_name, "O": o_name}
        self.scores = {"X": 0, "O": 0}
        self.current_player = "X"
        self.game_active = True
        self._update_scoreboard()
        self._update_status_label(f"{self.players[self.current_player]}'s turn ({self.current_player}).")
        self._enable_board(True)
        self._clear_board_buttons()
        self.new_round_button.setEnabled(True)
        self.reset_scores_button.setEnabled(True)

    def make_move(self, index):
        if not self.game_active:
            return

        if self.board[index]:
            return

        self.board[index] = self.current_player
        self.cell_buttons[index].setText(self.current_player)
        self.cell_buttons[index].setDisabled(True)

        winner = self._check_winner()
        if winner:
            self.scores[winner] += 1
            self._update_scoreboard()
            self._update_status_label(f"{self.players[winner]} wins! ({winner})")
            self.game_active = False
            self.new_round_button.setEnabled(True)
            return

        if all(self.board):
            self._update_status_label("It’s a draw. Start a new round.")
            self.game_active = False
            self.new_round_button.setEnabled(True)
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self._update_status_label(f"{self.players[self.current_player]}'s turn ({self.current_player}).")

    def _check_winner(self):
        winning_lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for a, b, c in winning_lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def reset_board(self):
        if not self.players["X"] or not self.players["O"]:
            return

        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        self._clear_board_buttons()
        self._enable_board(True)
        self._update_status_label(f"{self.players[self.current_player]}'s turn ({self.current_player}).")

    def reset_scores(self):
        self.scores = {"X": 0, "O": 0}
        self._update_scoreboard()
        self._update_status_label("Scores reset. Continue playing.")

    def _clear_board_buttons(self):
        for button in self.cell_buttons:
            button.setText("")
            button.setEnabled(True)

    def _enable_board(self, enabled):
        for button in self.cell_buttons:
            button.setEnabled(enabled and not button.text())

    def _update_scoreboard(self):
        self.score_label_x.setText(f"{self.players['X']}: {self.scores['X']}")
        self.score_label_o.setText(f"{self.players['O']}: {self.scores['O']}")

    def _update_status_label(self, message):
        self.status_label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    sys.exit(app.exec())
