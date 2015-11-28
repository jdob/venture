# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

from venture.engine.context import game
from venture.maps.tomb import Tomb


class TombTests(unittest.TestCase):

    def setUp(self):
        super(TombTests, self).setUp()
        self.config = game().config

    def test_calculate_size_no_corridors(self):
        # Test
        room_size, total_size = self._run_calculate(5, 0, 100, 100)

        # Verify
        self.assertEqual(19, room_size)
        self.assertEqual(95, total_size)

    def test_calculate_size_corridors(self):
        # Test
        room_size, total_size = self._run_calculate(5, 1, 100, 100)

        # Verify
        # Room size = 100 / (5 rooms + 1 corridor tile)
        self.assertEqual(19, room_size)
        self.assertEqual(99, total_size)


    def _run_calculate(self, grid_size, corridor_size,
                       map_width, map_height):
        self.config.map_width = map_width
        self.config.map_height = map_height

        grid_size = grid_size
        corridor_size = corridor_size

        # Test
        t = Tomb(grid_size, corridor_size)
        return t._calculate_room_size()
