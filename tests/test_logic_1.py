import unittest
from logic import SolitaireLogic

class TestSolitaire(unittest.TestCase):
    def setUp(self):
        self.game = SolitaireLogic()

    def test_initial_peg_count(self):
        self.assertEqual(self.game.peg_count, 32, "The initial number of pieces should be 32.")

    def test_jump_validation(self):
        self.assertTrue(self.game.is_valid_jump(2))
        self.assertFalse(self.game.is_valid_jump(3))

if __name__ == '__main__':
    unittest.main()