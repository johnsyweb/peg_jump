#!/usr/bin/env python
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

import game    # unit to test
import unittest # unit test framework   

class FakeStdOut:
        def __init__(self):
                self.reset()

        def write(self, text):
                self.buffer += text

        def reset(self):
                self.buffer = ''

class FakeStdIn:
        def __init__(self):
                self.lines = []

        def readline(self):
                return self.lines.pop(0)

class TestGame(unittest.TestCase):

        def setUp(self):
                self.fake_std_out = FakeStdOut()
                self.fake_std_in = FakeStdIn()
                self.game = game.Game(input = self.fake_std_in, output = self.fake_std_out)

        def start_game_with_top_peg_removed(self):
                '''
                Helper function. Starts the game and removes the top peg.
                '''
                self.game.start()
                self.fake_std_in.lines.append('0, 0\n')
                self.game.remove_first_peg()

        def test_fresh_game_has_full_board(self):
                self.assertEquals(self.game.board.peg_count(), 15)

        def test_welcome_message_emitted(self):
                self.game.welcome()
                self.assertTrue('Welcome to Peg Jump.' in self.fake_std_out.buffer)

        def test_start_game_displays_board(self):
                self.game.start()
                self.assertTrue('''
      /\\
     / x \\
    / x  x \\
   / x  x  x \\
  / x  x  x  x \\
 / x  x  x  x  x \\
+-----------------+''' in self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)

        def test_prompt_at_game_start(self):
                self.game.start()
                self.assertTrue('Please select a peg to remove(row, column):' in 
                                self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)

        def test_get_valid_peg_position(self):
                self.fake_std_in.lines.append('0, 0\n')
                row, column = self.game.get_valid_peg_position()

        def test_can_remove_first_peg(self):
                self.start_game_with_top_peg_removed()
                self.assertTrue(self.game.board.is_vacant(0, 0))

        def test_empty_string_raises_exception(self):
                self.fake_std_in.lines.append('')
                self.assertRaises(Exception, self.game.get_valid_peg_position)

        def test_three_numbers_raise_exception(self):
                self.fake_std_in.lines.append('1, 2, 3\n')
                self.assertRaises(Exception, self.game.get_valid_peg_position)

        def test_a_valid_peg_can_be_entered_after_invalid(self):
                self.game.start()
                self.fake_std_in.lines.append('-1, -1\n')
                self.fake_std_in.lines.append('0, 0\n')
                self.game.remove_first_peg()
                self.assertTrue(self.game.board.is_vacant(0, 0))

        def test_peg_removal_draws_board(self):
                self.start_game_with_top_peg_removed()
                self.assertTrue('''
      /\\
     / . \\
    / x  x \\
   / x  x  x \\
  / x  x  x  x \\
 / x  x  x  x  x \\
+-----------------+''' in self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)


        def test_get_source_peg(self):
                self.start_game_with_top_peg_removed()
                self.fake_std_in.lines.append('2, 2\n')
                row, column = self.game.get_populated_peg_position()
                self.assertEquals(2, row)
                self.assertEquals(2, column)

        def test_get_target_hole(self):
                self.start_game_with_top_peg_removed()
                self.fake_std_in.lines.append('0, 0\n')
                row, column = self.game.get_unpopulated_peg_position()
                self.assertEquals(0, row)
                self.assertEquals(0, column)



if __name__ == '__main__':
        unittest.main()
