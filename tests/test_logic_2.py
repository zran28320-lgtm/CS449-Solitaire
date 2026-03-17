import unittest
from logic import SolitaireLogic


class TestSolitaire(unittest.TestCase):
    def setUp(self):
        """Initialize a fresh game logic instance before each test."""
        self.game = SolitaireLogic()
        self.game.set_board_parameters("7", "English")
        self.game.start_new_game()

    # ================= User Story 1 =================
    def test_ac_1_1_valid_board_size(self):
        # AC 1.1 <Valid board size input>
        result = self.game.set_board_parameters("9", "English")
        self.assertTrue(result)
        self.assertEqual(self.game.board_size, 9)

    def test_ac_1_2_invalid_board_size(self):
        # AC 1.2 <Invalid board size input>
        result = self.game.set_board_parameters("-5", "English")
        self.assertFalse(result)
        # Verify it maintains previous valid size (7)
        self.assertEqual(self.game.board_size, 7)

    def test_ac_1_4_change_type_hexagon(self):
        # AC 1.4 <Change board type to Hexagon>
        self.game.set_board_parameters("7", "Hexagon")
        self.assertEqual(self.game.board_type, "Hexagon")

    def test_ac_1_5_change_type_diamond(self):
        # AC 1.5 <Change board type to Diamond>
        self.game.set_board_parameters("7", "Diamond")
        self.assertEqual(self.game.board_type, "Diamond")

    # ================= User Story 2 =================
    def test_ac_2_1_initial_board_state(self):
        # AC 2.1 <Initial board state generation>
        # English board size 7 should have 32 pegs and 1 empty center
        self.assertEqual(self.game.pegs_left, 32)
        self.assertEqual(self.game.grid[3][3], 2)  # Center is empty (2)
        self.assertEqual(self.game.grid[3][2], 1)  # Adjacent is peg (1)

    def test_ac_2_2_reset_ongoing_game(self):
        # AC 2.2 <Resetting an ongoing game>
        # Make a move to alter the state
        self.game.execute_move(3, 1, 3, 3)
        self.assertEqual(self.game.pegs_left, 31)  # Changed state

        # Reset game
        self.game.start_new_game()
        self.assertEqual(self.game.pegs_left, 32)  # Reset to full
        self.assertEqual(self.game.grid[3][3], 2)  # Center is empty again

    # ================= User Story 3 =================
    def test_ac_3_1_valid_jump(self):
        # AC 3.1 <A valid jump move> (From ChatGPT Fix)
        initial_pegs = self.game.pegs_left
        result = self.game.execute_move(3, 1, 3, 3)
        self.assertTrue(result)
        self.assertEqual(self.game.grid[3][1], 2)  # Start empty
        self.assertEqual(self.game.grid[3][2], 2)  # Middle empty
        self.assertEqual(self.game.grid[3][3], 1)  # Target filled
        self.assertEqual(self.game.pegs_left, initial_pegs - 1)

    def test_ac_3_2_invalid_occupied_target(self):
        # AC 3.2 <An invalid move on an occupied target hole>
        # Jump from (3,0) over (3,1) to (3,2). Target (3,2) is occupied (1).
        result = self.game.execute_move(3, 0, 3, 2)
        self.assertFalse(result)

    def test_ac_3_3_invalid_empty_adjacent(self):
        # AC 3.3 <An invalid move over an empty adjacent hole>
        # Manually clear the middle peg to simulate empty adjacent
        self.game.grid[3][2] = 2
        # Attempt to jump from (3,1) to (3,3) over (3,2)
        result = self.game.execute_move(3, 1, 3, 3)
        self.assertFalse(result)

    def test_ac_3_4_invalid_out_of_bounds(self):
        # AC 3.4 <An invalid move outside the board> (From ChatGPT Fix)
        result = self.game.execute_move(2, 0, 2, -2)
        self.assertFalse(result)

    # ================= User Story 4 =================
    def test_ac_4_1_rating_outstanding(self):
        # AC 4.1 <Game over with Outstanding rating>
        self.game.pegs_left = 1
        self.assertEqual(self.game.get_game_rating(), "Outstanding")

    def test_ac_4_2_rating_very_good(self):
        # AC 4.2 <Game over with Very Good rating>
        self.game.pegs_left = 2
        self.assertEqual(self.game.get_game_rating(), "Very Good")

    def test_ac_4_3_rating_good(self):
        # AC 4.3 <Game over with Good rating>
        self.game.pegs_left = 3
        self.assertEqual(self.game.get_game_rating(), "Good")

    def test_ac_4_4_rating_average(self):
        # AC 4.4 <Game over with Average rating>
        self.game.pegs_left = 5
        self.assertEqual(self.game.get_game_rating(), "Average")

    def test_ac_4_5_continuing_game(self):
        # AC 4.5 <A continuing game after a move>
        # A fresh board definitely has valid moves
        self.assertTrue(self.game.has_any_valid_moves())

        # Setup a scenario with NO valid moves (clear board, add 1 peg)
        self.game.grid = [[2 for _ in range(7)] for _ in range(7)]
        self.game.grid[3][3] = 1  # Only one peg left
        self.assertFalse(self.game.has_any_valid_moves())


if __name__ == '__main__':
    unittest.main()