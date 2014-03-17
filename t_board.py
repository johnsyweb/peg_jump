#!/usr/bin/env python
'''
Test cases for board.Board
'''

import board
import unittest


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()

    def test_blank_board_has_no_pegs(self):
        self.assertEquals(self.board.peg_count(), 0)

    def test_can_win_easy_in_one_move(self):
        self.board.pegs.append((4, 3))
        self.board.pegs.append((4, 4))
        move_list = self.board.auto_play_move()
        self.assertTrue(self.board.game_over())
        self.assertEquals(move_list, [(4, 4, 4, 2)])

    def test_can_win_easy_in_two_moves(self):
        self.board.pegs.append((4, 1))
        self.board.pegs.append((4, 3))
        self.board.pegs.append((4, 4))
        move_list = self.board.auto_play_move()
        self.assertTrue(self.board.game_over())
        self.assertEquals(move_list, [(4, 4, 4, 2), (4, 1, 4, 3)])

    def test_can_win_easy_with_one_mistake(self):
        self.board.pegs.append((4, 1))
        self.board.pegs.append((4, 2))
        self.board.pegs.append((3, 0))
        move_list = self.board.auto_play_move()
        self.assertTrue(self.board.game_over())
        self.assertEquals(move_list, [(4, 2, 4, 0), (4, 0, 2, 0)])

    def test_game_won(self):
        self.board.pegs.append((0, 0))
        self.assertTrue(self.board.won())

    def test_print_empty_board(self):
        self.assertMultiLineEqual(self.board.__str__(), r'''
      /\
     / . \
    / .  . \
   / .  .  . \
  / .  .  .  . \
 / .  .  .  .  . \
+-----------------+
''')

    def test_two_moves_at_bottom_left(self):
        self.board.pegs.append((3, 0))
        self.board.pegs.append((4, 0))
        self.board.pegs.append((4, 1))
        self.assertEquals(len(self.board.get_valid_moves()), 2)

    def test_two_moves_at_bottom_right(self):
        self.board.pegs.append((3, 3))
        self.board.pegs.append((4, 3))
        self.board.pegs.append((4, 4))
        self.assertEquals(len(self.board.get_valid_moves()), 2)

    def test_two_moves_at_top(self):
        self.board.pegs.append((0, 0))
        self.board.pegs.append((1, 0))
        self.board.pegs.append((1, 1))
        self.assertEquals(len(self.board.get_valid_moves()), 2)


class TestBoardAfterReset(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.board.reset()

    def test_reset_board_has_15_pegs(self):
        self.assertEquals(self.board.peg_count(), 15)

    def test_only_valid_remove_allowed(self):
        self.assertRaises(Exception, self.board.remove_peg, row=6, column=0)
        self.assertEquals(self.board.peg_count(), 15)

    def test_full_board(self):
        self.assertTrue(self.board.is_full())

    def test_full_board_is_not_over(self):
        self.assertFalse(self.board.game_over())

    def test_invalid_move_target_out_of_bounds(self):
        self.assertFalse(self.board.is_valid_move(1, 0, -1, 0))

    def test_no_valid_moves_on_full_board(self):
        self.assertEquals(len(self.board.get_valid_moves()), 0)


class TestBoardWithTopPegRemoved(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.board.reset()
        self.board.remove_peg(0, 0)

    def test_removing_peg_reduces_peg_count(self):
        self.assertEquals(self.board.peg_count(), 14)

    def test_only_one_remove_allowed(self):
        self.assertRaises(Exception, self.board.remove_peg, row=2, column=0)
        self.assertEquals(self.board.peg_count(), 14)

    def test_vacant_hole_after_remove_top_peg(self):
        self.assertTrue(self.board.is_vacant(0, 0))

    def test_is_vacant_on_filled_hole(self):
        self.assertFalse(self.board.is_vacant(1, 1))

    def test_is_vacant_on_invalid_hole(self):
        self.assertFalse(self.board.is_vacant(0, -1))

    def test_valid_move_after_remove_top_peg(self):
        self.assertTrue(self.board.is_valid_move(2, 0, 0, 0))

    def test_valid_move_across_rows_and_columns(self):
        self.assertTrue(self.board.is_valid_move(2, 2, 0, 0))

    def test_invalid_move_no_peg_at_source(self):
        self.assertFalse(self.board.is_valid_move(0, 0, 0, 2))

    def test_invalid_move_peg_at_target(self):
        self.assertFalse(self.board.is_valid_move(2, 0, 4, 0))

    def test_invalid_move_no_middle_peg(self):
        self.board.pegs.remove((1, 0))
        self.assertFalse(self.board.is_valid_move(2, 0, 0, 0))

    def test_invalid_move_target_too_far(self):
        self.assertFalse(self.board.is_valid_move(4, 0, 0, 0))

    def test_valid_move_fills_target_hole(self):
        self.board.move(2, 0, 0, 0)
        self.assertFalse(self.board.is_vacant(0, 0))

    def test_valid_move_vacates_source_hole(self):
        self.board.move(2, 0, 0, 0)
        self.assertTrue(self.board.is_vacant(2, 0))

    def test_valid_move_vacates_middle_hole(self):
        self.board.move(2, 0, 0, 0)
        self.assertTrue(self.board.is_vacant(1, 0))

    def test_valid_move_reduces_peg_count(self):
        self.board.move(2, 0, 0, 0)
        self.assertEquals(self.board.peg_count(), 13)

    def test_invalid_move_fails(self):
        self.board.move(4, 0, 0, 0)
        self.assertEquals(self.board.peg_count(), 14)

    def test_remove_peg_sets_move_list(self):
        self.assertListEqual(self.board.move_list, [(0, 0)])

    def test_valid_move_sets_move_list(self):
        self.board.move(2, 2, 0, 0)
        self.assertListEqual(self.board.move_list, [(0, 0), (2, 2, 0, 0)])

    def test_two_valid_moves_set_move_list(self):
        self.board.move(2, 2, 0, 0)
        self.board.move(3, 1, 1, 1)
        self.assertListEqual(self.board.move_list,
                             [(0, 0), (2, 2, 0, 0), (3, 1, 1, 1)])

    def test_two_valid_moves_after_removing_top(self):
        self.assertEquals(len(self.board.get_valid_moves()), 2)

    def test_game_not_won(self):
        self.board.pegs.append((0, 0))
        self.board.pegs.append((2, 0))
        self.assertFalse(self.board.won())

    def test_game_over(self):
        self.board.pegs.append((0, 0))
        self.board.pegs.append((2, 0))
        self.assertTrue(self.board.game_over())

    def test_print_empty_board_of_three_rows(self):
        self.board = board.Board(3)
        self.assertEquals(self.board.__str__(), r'''
    /\
   / . \
  / .  . \
 / .  .  . \
+-----------+
''')

    def test_print_board(self):
        self.assertEquals(self.board.__str__(), r'''
      /\
     / . \
    / x  x \
   / x  x  x \
  / x  x  x  x \
 / x  x  x  x  x \
+-----------------+
''')

    def test_undo_replaces_pegs(self):
        self.board.move(2, 2, 0, 0)
        self.board.move(3, 1, 1, 1)
        peg_count = self.board.peg_count()
        self.board.undo()
        self.assertEquals(self.board.peg_count(), peg_count + 1)
        self.assertTrue(self.board.is_vacant(1, 1))
        self.assertFalse(self.board.is_vacant(3, 1))
        self.assertFalse(self.board.is_vacant(2, 1))

    def test_can_win_full_game(self):
        self.assertEquals(len(self.board.auto_play_move()), 14)
        self.assertTrue(self.board.won())

    def test_board_size_calculation(self):
        self.assertEquals(self.board.size(), 15)

    def test_reset_resets_board(self):
        self.board.reset()
        self.assertEquals(len(self.board.pegs), 15)
        self.assertListEqual(self.board.move_list, [])


class TestDemo(unittest.TestCase):
    @unittest.skip('''This function takes far too long for a unit test, but is
                   quite fun to watch.''')
    def test_can_win_full_game_with_any_peg_removed(self):
        test = board.Board()
        for row in xrange(5):
            for column in xrange(row):
                test.reset()
                test.remove_peg(row, column)
                self.assertEquals(len(test.auto_play_move(True)), 14)
                self.assertTrue(test.won())

if __name__ == '__main__':
    unittest.main()
