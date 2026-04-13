import random
import json


class SolitaireGame:
    def __init__(self):
        self.board_size = 7
        self.board_type = "English"
        self.grid = []
        self.pegs_left = 0
        self.is_recording = False
        self.history = []

    def set_recording(self, is_recording):
        self.is_recording = is_recording

    def set_board_parameters(self, size_str, board_type):
        try:
            size = int(size_str)
            if size < 3 or size % 2 == 0:
                raise ValueError("Size must be an odd positive integer.")
            self.board_size = size
            self.board_type = board_type
            return True
        except ValueError:
            return False

    def start_new_game(self):
        self.grid = self._generate_board()
        self.pegs_left = sum(row.count(1) for row in self.grid)

        if self.is_recording:
            mode = "Automated" if isinstance(self, AutomatedGame) else "Manual"
            self.history = [f"INIT|{self.board_size}|{self.board_type}|{mode}"]

        return True

    def _is_valid_slot(self, r, c):
        size = self.board_size
        center = size // 2
        if self.board_type == "English":
            arm_width = size // 3
            margin = (size - arm_width) // 2
            return (margin <= r < size - margin) or (margin <= c < size - margin)
        elif self.board_type == "Diamond":
            return abs(r - center) + abs(c - center) <= center
        elif self.board_type == "Hexagon":
            return abs(r - center) + abs(c - center) <= center + (center // 2)
        return False

    def _generate_board(self):
        size = self.board_size
        grid = [[0 for _ in range(size)] for _ in range(size)]
        center = size // 2

        for r in range(size):
            for c in range(size):
                if self._is_valid_slot(r, c):
                    grid[r][c] = 1

        grid[center][center] = 2
        return grid

    def validate_move(self, sr, sc, er, ec):
        if not (0 <= sr < self.board_size and 0 <= sc < self.board_size and
                0 <= er < self.board_size and 0 <= ec < self.board_size):
            return False
        if self.grid[sr][sc] != 1 or self.grid[er][ec] != 2:
            return False

        dr, dc = er - sr, ec - sc
        if (abs(dr) == 2 and dc == 0) or (abs(dc) == 2 and dr == 0) or (abs(dr) == 2 and abs(dc) == 2):
            mr, mc = sr + dr // 2, sc + dc // 2
            if self.grid[mr][mc] == 1:
                return True
        return False

    def execute_move(self, sr, sc, er, ec, is_replay=False):
        if self.validate_move(sr, sc, er, ec):
            mr, mc = sr + (er - sr) // 2, sc + (ec - sc) // 2
            self.grid[sr][sc] = 2
            self.grid[er][ec] = 1
            self.grid[mr][mc] = 2
            self.pegs_left -= 1

            if self.is_recording and not is_replay:
                self.history.append(f"MOVE|{sr}|{sc}|{er}|{ec}")

            return True
        return False

    def get_all_valid_moves(self):
        size = self.board_size
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2), (2, -2), (-2, 2)]
        valid_moves = []
        for r in range(size):
            for c in range(size):
                if self.grid[r][c] == 1:
                    for dr, dc in directions:
                        if self.validate_move(r, c, r + dr, c + dc):
                            valid_moves.append((r, c, r + dr, c + dc))
        return valid_moves

    def has_any_valid_moves(self):
        return len(self.get_all_valid_moves()) > 0

    def get_game_rating(self):
        if self.pegs_left == 1:
            return "Outstanding"
        elif self.pegs_left == 2:
            return "Very Good"
        elif self.pegs_left == 3:
            return "Good"
        else:
            return "Average"

    def save_record(self, filepath):
        with open(filepath, 'w') as f:
            for line in self.history:
                f.write(line + '\n')


class ManualGame(SolitaireGame):
    def randomize_board(self, is_replay=False, grid_state=None):
        if is_replay and grid_state:
            self.grid = grid_state
            self.pegs_left = sum(row.count(1) for row in self.grid)
            return True

        valid_slots = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self._is_valid_slot(r, c):
                    valid_slots.append((r, c))
                    self.grid[r][c] = 2
                else:
                    self.grid[r][c] = 0

        chosen_slots = random.sample(valid_slots, min(self.pegs_left, len(valid_slots)))
        for r, c in chosen_slots:
            self.grid[r][c] = 1

        if self.is_recording and not is_replay:
            self.history.append(f"RANDOMIZE|{json.dumps(self.grid)}")

        return True


class AutomatedGame(SolitaireGame):
    def make_automated_move(self):
        possible_moves = self.get_all_valid_moves()
        if not possible_moves:
            return False

        move = random.choice(possible_moves)
        self.execute_move(*move)
        return True