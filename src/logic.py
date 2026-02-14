class SolitaireLogic:
    def __init__(self):
        self.board_size = 7
        self.peg_count = 32

    def reset_game(self):
        self.peg_count = 32
        return True

    def is_valid_jump(self, distance):
        return distance == 2