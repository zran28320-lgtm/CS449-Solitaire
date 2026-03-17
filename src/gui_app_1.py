import tkinter as tk
from logic import SolitaireLogic

class SolitaireGUI:
    def __init__(self, root):
        self.logic = SolitaireLogic()
        self.root = root
        self.root.title("CS 449 Solitaire - Sprint 0")
        self.root.geometry("650x450")

        # 1. Text
        tk.Label(root, text="Sample GUI of Solitaire", font=("Arial", 14)).place(x=20, y=10)

        # 2. Radio buttons
        tk.Label(root, text="Board Type:").place(x=20, y=60)
        self.board_var = tk.StringVar(value="English")
        tk.Radiobutton(root, text="English", variable=self.board_var, value="English").place(x=40, y=85)
        tk.Radiobutton(root, text="Hexagon", variable=self.board_var, value="Hexagon").place(x=40, y=110)

        # 3. Lines
        self.canvas = tk.Canvas(root, width=200, height=200, bg="white", highlightthickness=1)
        self.canvas.place(x=200, y=80)

        self.canvas.create_line(0, 66, 200, 66, fill="lightgray")
        self.canvas.create_line(0, 133, 200, 133, fill="lightgray")

        # 4. Check box
        self.record_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Record game", variable=self.record_var).place(x=20, y=400)
        tk.Button(root, text="New Game", command=self.reset).place(x=450, y=120)

    def reset(self):
        if self.logic.reset_game():
            print("Game Logic Reset!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()