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

class Test(unittest.TestCase):

        class FakeStdOut:
                def __init__(self):
                        self.buffer = ''

                def write(self, text):
                        self.buffer += text

        def setUp(self):
                self.fake_std_out = self.FakeStdOut()
                self.game = game.Game(output = self.fake_std_out)

        def test_fresh_game_has_full_board(self):
                self.assertEquals(self.game.board.peg_count(), 15)

        def test_welcome_message_emitted(self):
                self.assertEquals(self.fake_std_out.buffer, '            \n                Welcome to Peg Jump. \n                             \n')


