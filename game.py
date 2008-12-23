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
                print >> self.output, center('''
                Welcome to Peg Jump. 
                ====================
                ''', self.width)
                print >> self.output, self.board

        def get_valid_peg_position(self):
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
                # amount = populated ? 'no' : 'a'...
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
                return self.get_peg_position(populated = True, prompt = default_prompt)
                        
        def get_unpopulated_peg_position(self):
                return self.get_peg_position(populated = False, prompt = 'Please select a hole to move to (row, column): ')

        def make_move(self):
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
                row, column = self.get_populated_peg_position(default_prompt = 'Please select a peg to remove(row, column): ')
                self.board.remove_peg(row, column)

        def do_main_move(self):
                source_row, source_column = self.get_populated_peg_position()
                target_row, target_column = self.get_unpopulated_peg_position()
                self.board.move(source_row, source_column, target_row, target_column)

        def over(self):
                return self.board.game_over()

        def play(self):
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
        game.make_move()
        game.make_move()

if __name__ == '__main__':
        main()

