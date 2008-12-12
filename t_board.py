#!/usr/bin/env python
################################################################################
# $Id: $
# $Source: $
################################################################################
# 
# Copyright (c) 2008 Pete Johns <paj@johnsy.com>
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# this program (see the file COPYING); if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA
# 
################################################################################

import board    # unit to test
import unittest # unit test framework   

class TestBoard(unittest.TestCase):

        def setUp(self):
                self.board = board.Board()

        def remove_top_peg(self):
                self.board.populate()
                self.board.remove_peg(row = 0, column = 0)

        def test_blank_board_has_no_pegs(self):
                self.assertEquals(self.board.peg_count(), 0)

        def test_populated_board_has_15_pegs(self):
                self.board.populate()
                self.assertEquals(self.board.peg_count(), 15)

        def test_removing_peg_reduces_peg_count(self):
                self.remove_top_peg()
                self.assertEquals(self.board.peg_count(), 14)

        def test_only_one_remove_allowed(self):
                self.remove_top_peg()
                self.board.remove_peg(row = 1, column = 0)
                self.assertEquals(self.board.peg_count(), 14)

        def test_vacant_hole_after_remove_top_peg(self):
                self.remove_top_peg()
                self.assert_(self.board.is_vacant(0, 0))

        def test_valid_move_after_remove_top_peg(self):
                self.remove_top_peg()
                self.assert_(self.board.is_valid_move(2, 0, 0, 0))

        def test_valid_move_across_rows_and_columns(self):
                self.remove_top_peg()
                self.assert_(self.board.is_valid_move(2, 2, 0, 0))

        def test_invalid_move_no_peg_at_source(self):
                self.remove_top_peg()
                self.assert_(not self.board.is_valid_move(0, 0, 0, 2))

        def test_invalid_move_peg_at_target(self):
                self.remove_top_peg()
                self.assert_(not self.board.is_valid_move(2, 0, 4, 0))

        def test_invalid_move_no_middle_peg(self):
                self.remove_top_peg()
                self.board.pegs.remove((1, 0))
                self.assert_(not self.board.is_valid_move(2, 0, 0, 0))

        def test_invalid_move_target_out_of_bounds(self):
                self.board.populate()
                self.assert_(not self.board.is_valid_move(1, 0, -1, 0))

        def test_invalid_move_target_too_far(self):
                self.remove_top_peg()
                self.assert_(not self.board.is_valid_move(4, 0, 0, 0))

        def test_valid_move_fills_target_hole(self):
                self.remove_top_peg()
                self.board.move(2, 0, 0, 0)
                self.assert_(not self.board.is_vacant(0, 0))

        def test_valid_move_vacates_source_hole(self):
                self.remove_top_peg()
                self.board.move(2, 0, 0, 0)
                self.assert_(self.board.is_vacant(2, 0))

        def test_valid_move_vacates_middle_hole(self):
                self.remove_top_peg()
                self.board.move(2, 0, 0, 0)
                self.assert_(self.board.is_vacant(1, 0))

        def test_valid_move_reduces_peg_count(self):
                self.remove_top_peg()
                self.board.move(2, 0, 0, 0)
                self.assertEquals(self.board.peg_count(), 13)

        def test_invalid_move_fails(self):
                self.remove_top_peg()
                self.board.move(4, 0, 0, 0)
                self.assertEquals(self.board.peg_count(), 14)

        def test_remove_peg_populates_move_list(self):
                self.remove_top_peg()
                self.assertEquals(self.board.move_list, [(0, 0)])

        def test_valid_move_populates_move_list(self):
                self.remove_top_peg()
                self.board.move(2, 2, 0, 0)
                self.assertEquals(self.board.move_list, [(0, 0), (2, 2, 0, 0)])

        def test_two_valid_moves_populate_move_list(self):
                self.remove_top_peg()
                self.board.move(2, 2, 0, 0)
                self.board.move(3, 1, 1, 1)
                self.assertEquals(self.board.move_list, [(0, 0), (2, 2, 0, 0), (3, 1, 1, 1)])

        def test_two_moves_at_top(self):
                self.board.pegs.append((0, 0))
                self.board.pegs.append((1, 0))
                self.board.pegs.append((1, 1))
                self.assertEquals(len(self.board.get_valid_moves()), 2)

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

        def test_no_valid_moves_on_full_board(self):
                self.board.populate()
                self.assertEquals(len(self.board.get_valid_moves()), 0)

        def test_two_valid_moves_after_removing_top(self):
                self.remove_top_peg()
                self.assertEquals(len(self.board.get_valid_moves()), 2)

        def test_game_not_won(self):
                self.board.pegs.append((0, 0))
                self.board.pegs.append((2, 0))
                self.assert_(not self.board.won())

        def test_game_won(self):
                self.board.pegs.append((0, 0))
                self.assert_(self.board.won())

        def test_game_over(self):
                self.board.pegs.append((0, 0))
                self.board.pegs.append((2, 0))
                self.assert_(self.board.game_over())

        def test_print_board(self):
                self.remove_top_peg()
                # Escaped backslashes.
                self.assertEquals(self.board.__str__(), 
'''
      /\\
     / . \\
    / x  x \\
   / x  x  x \\
  / x  x  x  x \\
 / x  x  x  x  x \\
+-----------------+
''')

        def test_undo_replaces_pegs(self):
                self.remove_top_peg()
                self.board.move(2, 2, 0, 0)
                self.board.move(3, 1, 1, 1)
                peg_count = self.board.peg_count()
                self.board.undo()
                self.assertEquals(self.board.peg_count(), peg_count + 1)
                self.assert_(self.board.is_vacant(1, 1))
                self.assert_(not self.board.is_vacant(3, 1))
                self.assert_(not self.board.is_vacant(2, 1))

        def test_can_win_easy_in_one_move(self):
                self.board.pegs.append((4, 3))
                self.board.pegs.append((4, 4))
                move_list = self.board.auto_play_move()
                self.assert_(self.board.game_over())
                self.assertEquals(move_list, [(4, 4, 4, 2)])

        def test_can_win_easy_in_two_moves(self):
                self.board.pegs.append((4, 1))
                self.board.pegs.append((4, 3))
                self.board.pegs.append((4, 4))
                move_list = self.board.auto_play_move()
                self.assert_(self.board.game_over())
                self.assertEquals(move_list, [(4, 4, 4, 2), (4, 1, 4, 3)])

        def test_can_win_easy_with_one_mistake(self):
                self.board.pegs.append((4, 1))
                self.board.pegs.append((4, 2))
                self.board.pegs.append((3, 0))
                move_list = self.board.auto_play_move()
                self.assert_(self.board.game_over())
                self.assertEquals(move_list, [(4, 2, 4, 0), (4, 0, 2, 0)])

        def test_can_win_full_game(self):
                self.remove_top_peg()
                self.assertEquals(len(self.board.auto_play_move()), 14)
                self.assert_(self.board.won())

        def test_board_size_calculation(self):
                self.assertEquals(self.board.size(), 15)

if __name__ == '__main__':
        unittest.main()
