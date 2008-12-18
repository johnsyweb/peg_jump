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

from board import Board
from string import center
import sys

class Game:
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

        def welcome(self):
                print >> self.output, center('''
                Welcome to Peg Jump. 
                ====================
                ''', self.width)

        def start(self):
                print >> self.output, self.board
                print >> self.output, 'Please select a peg to remove(row, column): ', 

        def get_valid_peg_position(self):
                line = self.input.readline()
                try:
                        (row_str, column_str) = line.split(',')
                        row, column = int(row_str), int(column_str)
                        if self.board.is_within_bounds(row, column):
                                return row, column
                        else:
                                raise Exception('Sorry, "' + line.strip() + '" is outside my boundaries.')
                except ValueError:
                        raise Exception('Sorry, I do not understand "' + line.strip() + '".')

        def get_peg_position(self, populated):

                # amount = populated ? 'no' : 'a'...
                amount = populated and 'no' or 'a'

                try:
                        row, column = self.get_valid_peg_position()
                        if self.board.is_vacant(row, column) == populated:
                                raise Exception('Sorry, there is ' + amount + ' peg at "' + row + ', ' + column + '".')
                        else:
                                return row, column
                except Exception, e:
                        print >> self.output, e

        def get_populated_peg_position(self):
                return self.get_peg_position(True)
                        
        def get_unpopulated_peg_position(self):
                return self.get_peg_position(False)
                        
        def remove_first_peg(self):
                while self.board.size() == self.board.peg_count():
                        try:
                                row, column = self.get_populated_peg_position()
                                self.board.remove_peg(row, column)
                        except TypeError:
                                self.start()
                print >> self.output, self.board

                
def main(print_board = True):
        '''
        This function demonstrates a sample winning game.
        '''
        game = Game()
        game.welcome()
        game.start()
        game.remove_first_peg()

if __name__ == '__main__':
        main()

