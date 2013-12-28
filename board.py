#!/usr/bin/env python
###############################################################################
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
###############################################################################


class Board:
    '''
    This is the back-end to peg-jump. It is a board containing pegs and a
    list of moves.
    '''

    def __init__(self, number_of_rows=5):
        '''
        Sets up the instance with an empty board of 'number_of_rows' rows
        '''
        self.rows = number_of_rows
        self.__clear_lists()

    def reset(self):
        '''
        Makes the board new again. All moves are cleared and all pegs
        returned to their homes.
        '''
        self.__clear_lists()
        for row in range(self.rows):
            for column in range(row + 1):
                self.pegs.append((row, column))

    def size(self):
        '''
        Returns the number of holes in the board.
        '''
        return (self.rows * (self.rows + 1)) / 2

    def peg_count(self):
        '''
        Returns the number of populated holes in the board.
        '''
        return len(self.pegs)

    def is_full(self):
        '''
        Returns true if and only if there is a peg in each hole. That
        is, at the beginning of the game.
        '''
        return self.size() == self.peg_count()

    def remove_peg(self, row, column):
        '''
        Removes the peg at the specified location. Can only be called at
        the very beginning of a game.
        '''
        if self.peg_count() == self.size():
            if (row, column) in self.pegs:
                self.pegs.remove((row, column))
                self.move_list.append((row, column))
            else:
                raise Exception('There is no peg at %d, %d' % (row, column))
        else:
            raise Exception('Cannot remove another peg')

    def is_within_bounds(self, row, column):
        '''
        Validation for a target location.
        '''
        return row in range(self.rows) and column in range(row + 1)

    def is_vacant(self, row, column):
        '''
        Validation for a target location.
        '''
        return (self.is_within_bounds(row, column) and
                (row, column) not in self.pegs)

    def is_correct_distance(self, source_row, source_column,
                            target_row, target_column):
        '''
        Validation for a target location.
        '''
        valid_jumps = [(+2,  0), (+2, +2),
                       (0, -2), (0, +2),
                       (-2, -2), (-2,  0)]

        distance = target_row - source_row, target_column - source_column
        return distance in valid_jumps

    def middle_peg(self, source_row, source_column, target_row, target_column):
        '''
        Calculates the location of a peg between a source and target hole.
        '''
        return (
            (source_row + target_row) / 2, (source_column + target_column) / 2)

    def has_middle_peg(self, *args):
        '''
        Validation for a target location.
        '''
        return self.middle_peg(*args) in self.pegs

    def is_valid_move(self, source_row, source_column,
                      target_row, target_column):
        '''
        A valid move is one where:
            -       The source location contains a peg
            -       The target location is empty
            -       There is exactly one peg betwixt
        '''
        return ((source_row, source_column) in self.pegs
                and self.is_vacant(target_row, target_column)
                and self.is_correct_distance(source_row, source_column,
                                             target_row, target_column)
                and self.has_middle_peg(source_row, source_column,
                                        target_row, target_column)
                )

    def move(self, source_row, source_column, target_row, target_column):
        ''' Makes a move on the board only if it is valid '''
        if self.is_valid_move(source_row, source_column,
                              target_row, target_column):
            self.pegs.append((target_row, target_column))
            self.pegs.remove((source_row, source_column))
            self.pegs.remove(self.middle_peg(source_row, source_column,
                                             target_row, target_column))
            self.move_list.append((source_row, source_column,
                                   target_row, target_column))

    def undo(self):
        ''' Undoes the last move '''
        last = self.move_list.pop()
        source_row, source_column, target_row, target_column = last
        self.pegs.remove((target_row, target_column))
        self.pegs.append((source_row, source_column))
        self.pegs.append(self.middle_peg(*last))

    def get_valid_moves(self):
        ''' Returns a list of all moves that can be made '''
        valid_moves = []
        for row, column in self.pegs:
            for r in (-2, 0, 2):
                for c in (-2, 0, 2):
                    target = row, column, row + r, column + c
                    if self.is_valid_move(*target):
                        valid_moves.append(target)
        return valid_moves

    def game_over(self):
        '''
        The game is over when no more moves can be executed.
        '''
        return not self.is_full() and not self.get_valid_moves()

    def won(self):
        ''' The object of the game is to get down to one peg. '''
        return self.peg_count() == 1

    def auto_play_move(self, print_board=False):
        ''' A recursive function that will search for a move_list that wins the
        game. '''
        for valid_move in self.get_valid_moves():
            self.move(*valid_move)
            if print_board:
                print self, valid_move
            if not self.game_over():
                self.auto_play_move(print_board)
            if self.won():
                return self.move_list
            self.undo()

    def __str__(self):
        ''' Returns an ASCII-art representation of the board '''
        spaces = self.rows + 1
        retstring = '\n'
        retstring += spaces * ' ' + '/\\\n'

        for row in range(self.rows):
            spaces -= 1
            retstring += spaces * ' ' + '/'
            for column in range(row + 1):
                if self.is_vacant(row, column):
                    retstring += ' . '
                else:
                    retstring += ' x '
            retstring += '\\\n'
        retstring += '+' + (self.rows * 3 + 2) * '-' + '+\n'
        return retstring

    def __clear_lists(self):
        self.pegs = []
        self.move_list = []


def main(print_board=True):
    '''
    This function demonstrates a sample winning game.
    '''
    board = Board()
    board.reset()
    board.remove_peg(row=0, column=0)
    board.auto_play_move(print_board)
    print board.move_list


if __name__ == '__main__':
    main()
