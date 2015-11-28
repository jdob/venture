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

from venture.engine.game import game


class Map(dict):

    def __init__(self, iterable=None, **kwargs):
        super(Map, self).__init__(iterable=iterable, **kwargs)
        self._map = None
        self._rooms = []

    def __getitem__(self, key):
        # shortcut to access tiles directly
        return self._map[key]

    @property
    def rooms(self):
        return list(self._rooms)

    def generate(self):
        config = game().config

        # Block everything by default
        self._map = [[Tile(block_move=True)
                      for y in range(config.map_height)]
                     for x in range(config.map_width)]

    def player_start_location(self):
        config = game().config

        # Ghetto implementation: return the first usable tile
        for x in range(config.map_width):
            for y in range(config.map_height):
                if not self._map[x][y].block_move:
                    return x, y

    def create_room(self, room):
        self._rooms.append(room)
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self._map[x][y].unblock()

    def create_horizontal_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self._map[x][y].unblock()

    def create_vertical_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self._map[x][y].unblock()


class Room:

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Tile:

    def __init__(self, block_move=False, block_sight=None):
        self.block_move = block_move

        if block_sight is None:
            block_sight = block_move
        self.block_sight = block_sight

        self.explored = False

    def block(self):
        self.block_move = True
        self.block_sight = True

    def unblock(self):
        self.block_move = False
        self.block_sight = False
