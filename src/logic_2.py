# logic.py

class SolitaireLogic:
    """
    Handles the pure game logic for Peg Solitaire.
    0: Out of bounds / Invalid
    1: Peg (Marble)
    2: Empty Hole
    """

    def __init__(self):
        self.board_size = 7
        self.board_type = "English"
        self.grid = []
        self.pegs_left = 0

    def set_board_parameters(self, size_str, board_type):
        """
        Handles AC 1.1, AC 1.2, AC 1.4, AC 1.5.
        Validates input and updates parameters for the NEXT game.
        """
        try:
            size = int(size_str)
            if size < 3 or size % 2 == 0:
                raise ValueError("Size must be an odd positive integer.")
            # Only update if valid (AC 1.1)
            self.board_size = size
            self.board_type = board_type
            return True
        except ValueError:
            # AC 1.2: Invalid input, maintain previous state
            return False

    def start_new_game(self):
        """
        Handles AC 2.1, AC 2.2.
        Discards current game and generates a new board based on current parameters.
        """
        self.grid = self._generate_board()

        # Count initial pegs
        self.pegs_left = sum(row.count(1) for row in self.grid)
        return True

    def _generate_board(self):
        """Generates the 2D grid based on size and type."""
        size = self.board_size
        grid = [[0 for _ in range(size)] for _ in range(size)]
        center = size // 2

        if self.board_type == "English":
            # Simple English cross generation
            arm_width = size // 3
            margin = (size - arm_width) // 2
            for r in range(size):
                for c in range(size):
                    if (margin <= r < size - margin) or (margin <= c < size - margin):
                        grid[r][c] = 1
        elif self.board_type == "Diamond":
            # Simplified Diamond logic for testing
            for r in range(size):
                for c in range(size):
                    if abs(r - center) + abs(c - center) <= center:
                        grid[r][c] = 1
        elif self.board_type == "Hexagon":
            # Simplified Hexagon logic for testing
            for r in range(size):
                for c in range(size):
                    grid[r][c] = 1

        # AC 2.1: Central hole remains empty
        grid[center][center] = 2
        return grid

    def validate_move(self, sr, sc, er, ec):
        """
        Handles AC 3.2, AC 3.3, AC 3.4.
        Checks if a move from (sr, sc) to (er, ec) is legal.
        """
        # AC 3.4: Invalid move outside the board
        if not (0 <= sr < self.board_size and 0 <= sc < self.board_size and
                0 <= er < self.board_size and 0 <= ec < self.board_size):
            return False

        # Start must be peg, end must be empty (AC 3.2: Target occupied check)
        if self.grid[sr][sc] != 1 or self.grid[er][ec] != 2:
            return False

        dr = er - sr
        dc = ec - sc

        # Check if it is a valid jump distance (orthogonal or diagonal)
        if (abs(dr) == 2 and dc == 0) or (abs(dc) == 2 and dr == 0) or (abs(dr) == 2 and abs(dc) == 2):
            mr, mc = sr + dr // 2, sc + dc // 2
            # AC 3.3: Invalid move over an empty adjacent hole
            if self.grid[mr][mc] == 1:
                return True

        return False

    def execute_move(self, sr, sc, er, ec):
        """
        Handles AC 3.1.
        Moves the peg and removes the jumped peg.
        """
        if self.validate_move(sr, sc, er, ec):
            mr, mc = sr + (er - sr) // 2, sc + (ec - sc) // 2
            self.grid[sr][sc] = 2  # Start becomes empty
            self.grid[er][ec] = 1  # Target gets the peg
            self.grid[mr][mc] = 2  # Jumped peg is removed
            self.pegs_left -= 1
            return True
        return False

    def has_any_valid_moves(self):
        """
        Handles AC 4.5.
        Scans the board to see if any valid move is possible.
        """
        size = self.board_size
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2), (2, -2), (-2, 2)]

        for r in range(size):
            for c in range(size):
                if self.grid[r][c] == 1:
                    for dr, dc in directions:
                        if self.validate_move(r, c, r + dr, c + dc):
                            return True
        return False

    def get_game_rating(self):
        """
        Handles AC 4.1, AC 4.2, AC 4.3, AC 4.4.
        Returns the final rating based on remaining pegs.
        """
        if self.pegs_left == 1:
            return "Outstanding"
        elif self.pegs_left == 2:
            return "Very Good"
        elif self.pegs_left == 3:
            return "Good"
        else:
            return "Average"