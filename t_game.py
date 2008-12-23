#!/usr/bin/env python
'''
 
 Copyright (c) 2008 Pete Johns <paj@johnsy.com>
 
 This program is free software; you can redistribute it and/or modify it under
 the terms of the GNU General Public License as published by the Free Software
 Foundation; either version 2, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 details.
 
 You should have received a copy of the GNU General Public License along with
 this program (see the file COPYING); if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA
 
'''

import game    # unit to test
import unittest # unit test framework   

class FakeStdOut:
        '''
        Fake class for testing output.
        '''
        def __init__(self):
                self.reset()

        def write(self, text):
                self.buffer += text

        def reset(self):
                self.buffer = ''

class FakeStdIn:
        '''
        Fake class for injecting input.
        '''
        def __init__(self):
                self.lines = []

        def readline(self):
                return self.lines.pop(0)

class TestGame(unittest.TestCase):
        '''
        Unit tests for the Game class. All TDD.
        '''

        def setUp(self):
                self.fake_std_out = FakeStdOut()
                self.fake_std_in = FakeStdIn()
                self.game = game.Game(input = self.fake_std_in, output = self.fake_std_out)

        def start_game_with_top_peg_removed(self):
                '''
                Helper function. Starts the game and removes the top peg.
                '''
                self.fake_std_in.lines.append('0, 0\n')
                self.game.make_move()

        def test_fresh_game_has_full_board(self):
                self.assertEquals(self.game.board.peg_count(), 15)

        def test_welcome_message_emitted(self):
                self.game.welcome()
                self.assertTrue('Welcome to Peg Jump.' in self.fake_std_out.buffer)

        def test_welcome_displays_board(self):
                self.game.welcome()
                self.assertTrue('''
      /\\
     / x \\
    / x  x \\
   / x  x  x \\
  / x  x  x  x \\
 / x  x  x  x  x \\
+-----------------+''' in self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)

        def test_prompt_at_game_start(self):
                self.start_game_with_top_peg_removed()
                self.assertTrue('Please select a peg to remove(row, column):' in 
                                self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)

        def test_get_valid_peg_position(self):
                self.fake_std_in.lines.append('0, 0\n')
                row, column = self.game.get_valid_peg_position()

        def test_can_make_move(self):
                self.start_game_with_top_peg_removed()
                self.assertTrue(self.game.board.is_vacant(0, 0))

        def test_empty_string_raises_exception(self):
                self.fake_std_in.lines.append('')
                self.assertRaises(Exception, self.game.get_valid_peg_position)

        def test_three_numbers_raise_exception(self):
                self.fake_std_in.lines.append('1, 2, 3\n')
                self.assertRaises(Exception, self.game.get_valid_peg_position)

        def test_a_valid_peg_can_be_entered_after_invalid(self):
                self.fake_std_in.lines.append('-1, -1\n')
                self.fake_std_in.lines.append('0, 0\n')
                self.game.make_move()
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

        def make_move_helper(self):
                self.start_game_with_top_peg_removed()
                self.fake_std_in.lines.append('2, 2\n')
                self.fake_std_in.lines.append('0, 0\n')
                self.fake_std_out.reset()
                self.game.make_move()

        def test_make_move_asks_for_source(self):
                self.make_move_helper()
                self.assertTrue('Please select a peg to move (row, column):' in self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)

        def test_make_move_asks_for_target(self):
                self.make_move_helper()
                self.assertTrue('Please select a hole to move to (row, column):' in self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)

        def test_make_move_draws_board(self):
                self.make_move_helper()
                self.assertTrue('''
      /\\
     / x \\
    / x  . \\
   / x  x  . \\
  / x  x  x  x \\
 / x  x  x  x  x \\
+-----------------+''' in self.fake_std_out.buffer, 'Unexpected output: ' + self.fake_std_out.buffer)

        def test_make_move_populates_move_list(self):
                self.make_move_helper()
                self.assertEquals(self.game.board.move_list[-1], (2, 2, 0, 0))

        def test_quit_command_exits_game_on_first_go(self):
                self.fake_std_in.lines.append('quit\n')
                self.game.make_move()

        def test_quit_command_exits_game_from_move(self):
                self.make_move_helper()
                self.fake_std_in.lines.append('quit\n')
                self.game.make_move()

        def test_invalid_input_rejected_and_move_made(self):
                self.make_move_helper()
                self.fake_std_in.lines.append('8, 8\n')
                self.fake_std_in.lines.append('2, 0\n')
                self.fake_std_in.lines.append('2, 2\n')
                self.game.make_move()
                self.assertTrue(self.game.board.is_vacant(2, 0))
                self.assertFalse(self.game.board.is_vacant(2, 2))

        def test_game_over(self):
                self.game.board.pegs = [(0, 0)]
                self.assertTrue(self.game.over())

        def test_game_over_is_reported_as_such(self):
                self.game.board.pegs = [(0, 0)]
                self.game.play()
                self.assertTrue('Game over.' in self.fake_std_out.buffer) 

        def test_loss_is_reported_as_such(self):
                self.game.board.pegs = [(0, 0), (4, 4)]
                self.game.play()
                self.assertTrue('You have lost.' in self.fake_std_out.buffer) 

        def test_win_is_reported_as_such(self):
                self.game.board.pegs = [(0, 0)]
                self.game.play()
                self.assertTrue('You have won!' in self.fake_std_out.buffer) 

        def test_sample_full_game(self):
                self.fake_std_in.lines.append('0, 0\n')
                self.fake_std_in.lines.append('2, 0\n')
                self.fake_std_in.lines.append('0, 0\n')
                self.fake_std_in.lines.append('2, 2\n')
                self.fake_std_in.lines.append('2, 0\n')
                self.fake_std_in.lines.append('3, 0\n')
                self.fake_std_in.lines.append('1, 0\n')
                self.fake_std_in.lines.append('4, 1\n')
                self.fake_std_in.lines.append('2, 1\n')
                self.fake_std_in.lines.append('4, 4\n')
                self.fake_std_in.lines.append('2, 2\n')
                self.fake_std_in.lines.append('4, 3\n')
                self.fake_std_in.lines.append('4, 1\n')
                self.fake_std_in.lines.append('4, 0\n')
                self.fake_std_in.lines.append('4, 2\n')
                self.fake_std_in.lines.append('0, 0\n')
                self.fake_std_in.lines.append('2, 0\n')
                self.fake_std_in.lines.append('1, 1\n')
                self.fake_std_in.lines.append('3, 3\n')
                self.fake_std_in.lines.append('4, 2\n')
                self.fake_std_in.lines.append('2, 2\n')
                self.fake_std_in.lines.append('3, 3\n')
                self.fake_std_in.lines.append('1, 1\n')
                self.fake_std_in.lines.append('2, 0\n')
                self.fake_std_in.lines.append('2, 2\n')
                self.fake_std_in.lines.append('1, 1\n')
                self.fake_std_in.lines.append('3, 3\n')
                self.game.play()
                self.assertTrue('You have won!' in self.fake_std_out.buffer) 


if __name__ == '__main__':
        unittest.main()
