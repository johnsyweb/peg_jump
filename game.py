#!/usr/bin/env python
"""

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
 
"""

from board import Board
from string import center
import sys

class InputException(Exception):
        pass

class QuitException(Exception):
        pass

class Game(object):
        '''
        This is the main game class. It provides an interactive CLI to the
        peg-jump game.
        '''

        def __init__(self, input = sys.stdin, output = sys.stdout):
                self.output = output
                self.input = input
                self.board = Board(5)
                self.board.reset()
                self.width = 80
                self.i = 0

        def welcome(self):
                '''
                Just a welcome message. Nothing special.
                '''

                print >> self.output, center('''
                Welcome to Peg Jump. 
                ====================
                ''', self.width)
                print >> self.output, self.board

        def get_valid_peg_position(self):
                '''
                Gets a valid peg position. Raises an InputException if it
                doesn't understand or a QuitException if 'quit' is entered.
                '''

                line = self.input.readline()
                if 'quit' in line:
                        raise QuitException
                try:
                        (row_str, column_str) = line.split(',')
                        row, column = int(row_str), int(column_str)
                        if self.board.is_within_bounds(row, column):
                                return row, column
                        else:
                                raise InputException('Sorry, "' + line.strip() + '" is outside my boundaries.')
                except ValueError:
                        raise InputException('Sorry, I do not understand "' + line.strip() + '".')

        def get_peg_position(self, populated, prompt = None):
                '''
                Wrapper for get_valid_peg_position, but knows about populated
                and unpopulated positions.
                '''
                amount = populated and 'no' or 'a'
                try:
                        print >> self.output, prompt,
                        row, column = self.get_valid_peg_position()
                        if self.board.is_vacant(row, column) == populated:
                                raise Exception('Sorry, there is ' + amount + ' peg at "' + row + ', ' + column + '".')
                        else:
                                return row, column
                except InputException, e:
                        print >> self.output, e

        def get_populated_peg_position(self, default_prompt = 'Please select a peg to move (row, column): '):
                '''
                Wrapper for get_peg_position. Sets appropriate prompt.
                '''
                return self.get_peg_position(populated = True, prompt = default_prompt)
                        
        def get_unpopulated_peg_position(self):
                '''
                Wrapper for get_peg_position. Sets appropriate prompt.
                '''
                return self.get_peg_position(populated = False, prompt = 'Please select a hole to move to (row, column): ')

        def make_move(self):
                '''
                Loops until valid input is supplied and then makes the move.
                Wraps do_first_move and do_main_move.
                '''
                target_count = self.board.peg_count() - 1
                while self.board.peg_count() is not target_count:
                        try:
                                if self.board.size() == self.board.peg_count():
                                        self.do_first_move()
                                else:
                                        self.do_main_move()
                        except QuitException, q:
                                print >> self.output, 'Goodbye.'
                                return
                        except TypeError:
                                print >> self.output, 'Please try again...'
                print >> self.output, self.board
                        
        def do_first_move(self):
                '''
                Code specific to clearing the first hole.
                '''
                row, column = self.get_populated_peg_position(default_prompt = 'Please select a peg to remove(row, column): ')
                self.board.remove_peg(row, column)

        def do_main_move(self):
                '''
                Code specific to moving a peg into a vacant hole.
                '''
                source_row, source_column = self.get_populated_peg_position()
                target_row, target_column = self.get_unpopulated_peg_position()
                self.board.move(source_row, source_column, target_row, target_column)

        def is_over(self):
                ''' 
                Returns True only if the game is over.
                '''
                return self.board.game_over()

        def play(self):
                '''
                Makes as many moves as is necessary to complete the game.
                '''
                while not self.is_over():
                        self.make_move()

                print >> self.output, 'Game over.'
                if self.board.won() is not True:
                        print >> self.output, 'You have lost.'
                else:
                        print >> self.output, 'You have won!'

def main(print_board = True):
        '''
        Play the game,
        (Play the game),
        '''
        game = Game()
        game.welcome()
        game.play()

if __name__ == '__main__':
        main()

