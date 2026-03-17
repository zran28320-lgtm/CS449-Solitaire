# gui_app.py
import tkinter as tk
from tkinter import messagebox
from logic import SolitaireLogic


class SolitaireGUI:
    def __init__(self, root):
        self.logic = SolitaireLogic()
        self.root = root
        self.root.title("CS 449 Solitaire - Sprint 2")
        self.root.geometry("650x550")

        self.selected_peg = None  # To track the first click (sr, sc)

        self._setup_ui()
        self.on_new_game_click()  # Start a default game on launch

    def _setup_ui(self):
        # Top Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Board Size
        tk.Label(control_frame, text="Board size:", font=("Arial", 12)).pack(side=tk.LEFT, padx=(20, 5))
        self.size_entry = tk.Entry(control_frame, width=5)
        self.size_entry.insert(0, "7")
        self.size_entry.pack(side=tk.LEFT)

        # Board Type
        self.board_var = tk.StringVar(value="English")
        tk.Label(control_frame, text="Board Type:").pack(side=tk.LEFT, padx=(20, 5))
        tk.Radiobutton(control_frame, text="English", variable=self.board_var, value="English").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Hexagon", variable=self.board_var, value="Hexagon").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Diamond", variable=self.board_var, value="Diamond").pack(side=tk.LEFT)

        # New Game Button
        tk.Button(control_frame, text="New Game", command=self.on_new_game_click, bg="lightgray").pack(side=tk.RIGHT,
                                                                                                       padx=20)

        # Canvas for the board
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_new_game_click(self):
        """Triggered by New Game button. Passes input to logic layer."""
        size_str = self.size_entry.get()
        board_type = self.board_var.get()

        # Try to set parameters in logic
        if self.logic.set_board_parameters(size_str, board_type):
            self.logic.start_new_game()
            self.selected_peg = None
            self.draw_board()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid odd integer for board size.")
            # AC 1.2: Restores the valid entry visually to match backend state
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(self.logic.board_size))

    def draw_board(self):
        self.canvas.delete("all")
        size = self.logic.board_size
        cell_size = 400 // size
        offset = 50

        for r in range(size):
            for c in range(size):
                val = self.logic.grid[r][c]
                if val != 0:  # 1 (Peg) or 2 (Empty)
                    x1 = offset + c * cell_size
                    y1 = offset + r * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size

                    # Draw grid square
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                    # Draw peg or hole
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    radius = cell_size // 3

                    if val == 1:
                        # Draw Peg (Black circle). Highlight if selected.
                        color = "red" if self.selected_peg == (r, c) else "black"
                        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=color)
                    elif val == 2:
                        # Draw Empty Hole (White circle with outline)
                        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline="gray")

    def on_canvas_click(self, event):
        """Handles player clicks for making moves."""
        size = self.logic.board_size
        cell_size = 400 // size
        offset = 50

        # Calculate clicked row and col
        c = (event.x - offset) // cell_size
        r = (event.y - offset) // cell_size

        # Check bounds
        if 0 <= r < size and 0 <= c < size and self.logic.grid[r][c] != 0:
            if self.selected_peg is None:
                # Select a peg
                if self.logic.grid[r][c] == 1:
                    self.selected_peg = (r, c)
                    self.draw_board()
            else:
                # Attempt to move
                sr, sc = self.selected_peg
                success = self.logic.execute_move(sr, sc, r, c)
                self.selected_peg = None  # Deselect after move attempt
                self.draw_board()

                if success:
                    self.check_game_over()

    def check_game_over(self):
        if not self.logic.has_any_valid_moves():
            rating = self.logic.get_game_rating()
            messagebox.showinfo("Game Over",
                                f"No more valid moves!\nYour Rating: {rating}\nPegs left: {self.logic.pegs_left}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()