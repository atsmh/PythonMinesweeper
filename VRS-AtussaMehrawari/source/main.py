"""
Verlassene Raumstation (Konsolen-Version).

Dieses Spiel simuliert das klassische Minesweeper-Spiel.
Das Spielfeld wird zufällig generiert und der Spieler gibt Koordinaten ein, um Felder aufzudecken.
"""

import random
from typing import List, Set, Tuple, Union


class Board:
    """Repräsentiert ein Minesweeper-Spielfeld mit Bomben und Spielmechanik."""

    def __init__(self, dim_size: int, num_bombs: int) -> None:
        self.dim_size: int = dim_size
        self.num_bombs: int = num_bombs
        self.board: List[List[Union[int, str]]] = self.make_new_board()
        self.assign_values_to_board()
        self.dug: Set[Tuple[int, int]] = set()

    def make_new_board(self) -> List[List[Union[int, str]]]:
        """Erstellt ein neues Spielfeld und platziert zufällig Bomben."""
        board: list[list[Union[int, str]]] = [
            [0 for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted: int = 0
        while bombs_planted < self.num_bombs:
            loc: int = random.randint(0, self.dim_size**2 - 1)
            row: int = loc // self.dim_size
            col: int = loc % self.dim_size
            if board[row][col] == '*':
                continue
            board[row][col] = '*'  # type: ignore[assignment] 
            bombs_planted += 1
        return board  # type: ignore[return-value]  

    def assign_values_to_board(self) -> None:
        """Zählt benachbarte Bomben für jedes Feld und speichert die Anzahl."""
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row: int, col: int) -> int:
        """Gibt die Anzahl der benachbarten Bomben eines Feldes zurück."""
        num_neighboring_bombs: int = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row: int, col: int) -> bool:
        """
        Deckt ein Feld auf. Wenn das Feld leer ist, wird rekursiv weitergegraben.
        Gibt False zurück, wenn eine Bombe getroffen wurde.
        """
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        val = self.board[row][col]
        if isinstance(val, int) and val > 0:
            return True

        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self) -> str:
        visible_board: List[List[str]] = [[' ' for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
        string_rep: str = ''
        indices: List[str] = [str(i) for i in range(self.dim_size)]
        indices_row: str = '   ' + '  '.join(indices) + '\n'
        for i, row_vals in enumerate(visible_board):
            string_rep += f'{i} |' + ' |'.join(row_vals) + ' |\n'
        return indices_row + '-' * len(indices_row) + '\n' + string_rep


def play(dim_size: int = 5, num_bombs: int = 5) -> None:
    """
    Startet das Spiel und führt die Spielschleife aus.
    Der Benutzer gibt Koordinaten ein, um Felder aufzudecken.
    Spielt weiter, bis eine Bombe getroffen oder alle sicheren Felder aufgedeckt sind.
    """
    while True:
        board: Board = Board(dim_size, num_bombs)
        safe: bool = True

        while len(board.dug) < board.dim_size ** 2 - num_bombs:
            print(board)
            try:
                user_input: str = input("Gib die Koordinaten zum Scannen des Spielfelds ein (Reihe, Spalte): ")
                row_str, col_str = user_input.split(',')
                row, col = int(row_str.strip()), int(col_str.strip())
                if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
                    print("Ungültige Position. Bitte versuche es erneut.")
                    continue
            except ValueError:
                print("Ungültiges Eingabeformat. Verwende: Reihe, Spalte.")
                continue

            safe = board.dig(row, col)
            if not safe:
                break

        if safe:
            print("🎉 GLÜCKWUNSCH!!!! DU HAST GEWONNEN!")
        else:
            print("💀 GAME OVER!")
            board.dug = {(r, c) for r in range(board.dim_size) for c in range(board.dim_size)}
            print(board)

        again: str = input("Möchtest du eine neue Runde spielen? (ja/nein): ").strip().lower()
        if again not in ["ja", "j", "yes", "y"]:
            print("Danke fürs Spielen!")
            break


if __name__ == '__main__':
    play()
