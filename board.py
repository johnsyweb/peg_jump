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

class Board:
        def __init__(self, number_of_rows = 5):
                self.pegs = []
                self.move_list = []
                self.rows = number_of_rows

        def populate(self):
                for row in range(self.rows):
                        for column in range(row + 1):
                                self.pegs.append((row, column))

        def size(self):
                return (self.rows * (self.rows + 1)) / 2

        def peg_count(self):
                return len(self.pegs)

        def remove_peg(self, row, column):
                if self.peg_count() == self.size():
                        self.pegs.remove((row, column))
                        self.move_list.append((row, column))


        def is_within_bounds(self, row, column):
                return row in range (self.rows) \
                        and column in range (row + 1)

        def is_vacant(self, row, column):
                return self.is_within_bounds(row, column) \
                        and (row, column) not in self.pegs
                        
        def is_correct_distance(self, source_row, source_column, target_row, target_column):
                valid_jumps = [(+2,  0), (+2, +2),
                               ( 0, -2), ( 0, +2), 
                               (-2, -2), (-2,  0)]

                return (target_row - source_row, target_column - source_column) in valid_jumps

        def middle_peg(self, source_row, source_column, target_row, target_column):
                return ((source_row + target_row) / 2, (source_column + target_column) / 2)

        def has_middle_peg(self, source_row, source_column, target_row, target_column):
                return self.middle_peg(source_row, source_column, target_row, target_column)in self.pegs

        def is_valid_move(self, source_row, source_column, target_row, target_column):
                return (source_row, source_column) in self.pegs \
                                and self.is_vacant(target_row, target_column) \
                                and self.is_correct_distance(source_row, source_column, target_row, target_column) \
                                and self.has_middle_peg(source_row, source_column, target_row, target_column)

        def move(self, source_row, source_column, target_row, target_column):
                if self.is_valid_move(source_row, source_column, target_row, target_column):
                        self.pegs.append((target_row, target_column))
                        self.pegs.remove((source_row, source_column))
                        self.pegs.remove(self.middle_peg(source_row, source_column, target_row, target_column))
                        self.move_list.append((source_row, source_column, target_row, target_column))

        def undo(self):
                (source_row, source_column, target_row, target_column) = self.move_list[-1]
                self.pegs.remove((target_row, target_column))
                self.pegs.append((source_row, source_column))
                self.pegs.append(self.middle_peg(source_row, source_column, target_row, target_column))
                self.move_list = self.move_list[:-1]
                        
        def get_valid_moves(self):
                valid_moves = [];
                for (source_row, source_column) in self.pegs:
                        for row in (-2, 0, 2):
                                for column in (-2, 0, 2):
                                        if self.is_valid_move(source_row, source_column, source_row + row, source_column + column):
                                                valid_moves.append((source_row, source_column, source_row + row, source_column + column))
                return valid_moves

        def game_over(self):
                return self.get_valid_moves() == []

        def won(self):
                return self.peg_count() == 1

        def auto_play_move(self, print_board = False):
                for valid_move in self.get_valid_moves():
                        self.move(valid_move[0], valid_move[1], valid_move[2], valid_move[3])
                        if print_board:
                                print self, valid_move
                        if not self.game_over():
                                self.auto_play_move(print_board)
                        if self.won():
                                return self.move_list
                        self.undo()

        def __str__(self):
                retstring = '\n      /\\\n';
                for row in range(self.rows):
                        spaces = '%%%ds' % (self.rows + 1 - row)
                        retstring += spaces % '/'
                        for column in range(row + 1):
                                if self.is_vacant(row, column):
                                        retstring += ' . '
                                else:
                                        retstring += ' x '
                        retstring += '\\\n'
                retstring += '+-----------------+\n'
                return retstring

def main():
        board = Board()
        board.populate()
        board.remove_peg(row = 0, column = 0)
        board.auto_play_move(print_board = True)
        print board.move_list


if __name__ == '__main__':
        main()

