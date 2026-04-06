import tkinter as tk
from tkinter import messagebox
import time
from logic import ManualGame, AutomatedGame


class SolitaireGUI:
    def __init__(self, root):
        self.logic = ManualGame()
        self.root = root
        self.root.title("CS 449 Solitaire - Sprint 3")
        self.root.geometry("700x550")

        self.selected_peg = None

        self._setup_ui()
        self.on_new_game_click()

    def _setup_ui(self):
        left_control_frame = tk.Frame(self.root)
        left_control_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        tk.Label(left_control_frame, text="Mode:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.mode_var = tk.StringVar(value="Manual")
        tk.Radiobutton(left_control_frame, text="Manual", variable=self.mode_var, value="Manual").grid(row=0, column=1,
                                                                                                       sticky="w")
        tk.Radiobutton(left_control_frame, text="Automated", variable=self.mode_var, value="Automated").grid(row=0,
                                                                                                             column=2,
                                                                                                             sticky="w")

        tk.Label(left_control_frame, text="Size:").grid(row=1, column=0, sticky="w", pady=5)
        self.size_entry = tk.Entry(left_control_frame, width=5)
        self.size_entry.insert(0, "7")
        self.size_entry.grid(row=1, column=1, sticky="w")

        tk.Label(left_control_frame, text="Type:").grid(row=1, column=2, sticky="e", padx=5)
        self.board_var = tk.StringVar(value="English")
        tk.Radiobutton(left_control_frame, text="English", variable=self.board_var, value="English").grid(row=1,
                                                                                                          column=3)
        tk.Radiobutton(left_control_frame, text="Hexagon", variable=self.board_var, value="Hexagon").grid(row=1,
                                                                                                          column=4)
        tk.Radiobutton(left_control_frame, text="Diamond", variable=self.board_var, value="Diamond").grid(row=1,
                                                                                                          column=5)

        self.canvas_size = 420
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=20, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        right_action_frame = tk.Frame(self.root)
        right_action_frame.pack(side=tk.LEFT, padx=20, pady=50, anchor="n")

        tk.Button(right_action_frame, text="New Game", command=self.on_new_game_click, width=12, bg="lightgray").pack(
            pady=10)
        tk.Button(right_action_frame, text="Autoplay", command=self.on_autoplay_click, width=12, bg="lightgray").pack(
            pady=10)
        tk.Button(right_action_frame, text="Randomize", command=self.on_randomize_click, width=12, bg="lightgray").pack(
            pady=10)

    def on_new_game_click(self):
        size_str = self.size_entry.get()
        board_type = self.board_var.get()
        mode = self.mode_var.get()

        if mode == "Manual":
            self.logic = ManualGame()
        else:
            self.logic = AutomatedGame()

        if self.logic.set_board_parameters(size_str, board_type):
            self.logic.start_new_game()
            self.selected_peg = None
            self.draw_board()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid odd integer for board size.")
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(self.logic.board_size))

    def on_randomize_click(self):
        if isinstance(self.logic, ManualGame):
            self.logic.randomize_board()
            self.selected_peg = None
            self.draw_board()
            self.check_game_over()
        else:
            messagebox.showinfo("Info", "Randomize is only available in Manual mode.")

    def on_autoplay_click(self):
        if not isinstance(self.logic, AutomatedGame):
            messagebox.showinfo("Info", "Please select 'Automated' mode and click 'New Game' first.")
            return

        while self.logic.has_any_valid_moves():
            self.logic.make_automated_move()
            self.draw_board()
            self.root.update()
            time.sleep(0.3)

        self.check_game_over()

    def draw_board(self):
        self.canvas.delete("all")
        size = self.logic.board_size

        offset = 30
        cell_size = (self.canvas_size - 2 * offset) // size

        for r in range(size):
            for c in range(size):
                val = self.logic.grid[r][c]
                if val != 0:
                    x1 = offset + c * cell_size
                    y1 = offset + r * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size

                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    radius = cell_size // 3
                    if val == 1:
                        color = "red" if self.selected_peg == (r, c) else "black"
                        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=color)
                    elif val == 2:
                        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline="gray")

    def on_canvas_click(self, event):
        if not isinstance(self.logic, ManualGame):
            return

        size = self.logic.board_size
        offset = 30
        cell_size = (self.canvas_size - 2 * offset) // size

        c, r = (event.x - offset) // cell_size, (event.y - offset) // cell_size

        if 0 <= r < size and 0 <= c < size and self.logic.grid[r][c] != 0:
            if self.selected_peg is None:
                if self.logic.grid[r][c] == 1:
                    self.selected_peg = (r, c)
                    self.draw_board()
            else:
                sr, sc = self.selected_peg
                success = self.logic.execute_move(sr, sc, r, c)
                self.selected_peg = None
                self.draw_board()
                if success:
                    self.check_game_over()

    def check_game_over(self):
        if not self.logic.has_any_valid_moves():
            rating = self.logic.get_game_rating()
            messagebox.showinfo("Game Over",
                                f"No more valid moves!\nRating: {rating}\nPegs left: {self.logic.pegs_left}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()