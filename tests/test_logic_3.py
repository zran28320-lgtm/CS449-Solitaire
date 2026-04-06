import unittest
from logic import ManualGame, AutomatedGame

class TestManualGame(unittest.TestCase):
    def setUp(self):
        self.game = ManualGame()
        self.game.set_board_parameters("7", "English")
        self.game.start_new_game()

    def test_ac_1_1_valid_board_size(self):
        result = self.game.set_board_parameters("9", "English")
        self.assertTrue(result)
        self.assertEqual(self.game.board_size, 9)

    def test_ac_1_2_invalid_board_size(self):
        result = self.game.set_board_parameters("-5", "English")
        self.assertFalse(result)
        self.assertEqual(self.game.board_size, 7)

    def test_ac_2_1_initial_board_state(self):
        self.assertEqual(self.game.pegs_left, 32)
        self.assertEqual(self.game.grid[3][3], 2)
        self.assertEqual(self.game.grid[3][2], 1)

    def test_ac_3_1_valid_jump(self):
        initial_pegs = self.game.pegs_left
        result = self.game.execute_move(3, 1, 3, 3)
        self.assertTrue(result)
        self.assertEqual(self.game.grid[3][1], 2)
        self.assertEqual(self.game.grid[3][3], 1)
        self.assertEqual(self.game.pegs_left, initial_pegs - 1)

    def test_ac_3_4_invalid_out_of_bounds(self):
        result = self.game.execute_move(2, 0, 2, -2)
        self.assertFalse(result)

    def test_randomize_board(self):
        self.game.execute_move(3, 1, 3, 3)
        pegs_before = self.game.pegs_left

        self.game.randomize_board()
        pegs_after = self.game.pegs_left

        self.assertEqual(pegs_before, pegs_after)

        actual_pegs = sum(row.count(1) for row in self.game.grid)
        self.assertEqual(actual_pegs, pegs_after)


class TestAutomatedGame(unittest.TestCase):
    def setUp(self):
        self.game = AutomatedGame()
        self.game.set_board_parameters("7", "English")
        self.game.start_new_game()

    def test_automated_move_execution(self):
        initial_pegs = self.game.pegs_left
        self.assertTrue(self.game.has_any_valid_moves())

        success = self.game.make_automated_move()
        self.assertTrue(success)

        self.assertEqual(self.game.pegs_left, initial_pegs - 1)

    def test_automated_game_finishes(self):
        moves = 0
        while self.game.has_any_valid_moves():
            self.game.make_automated_move()
            moves += 1
            if moves > 50:
                break

        self.assertFalse(self.game.has_any_valid_moves())


if __name__ == '__main__':
    unittest.main()