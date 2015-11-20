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

import sys

from venture.engine.context import get_context


class Objects(list):

    def at(self, x, y, blocks_movement=False):
        found = [o for o in self if o.x == x and o.y == y]
        if blocks_movement:
            found = [o for o in found if o.blocks_movement]

        if len(found) > 1:
            raise Exception('Multiple objects [%s] found at (%s, %s)'
                            % (len(found), x, y))
        elif len(found) == 1:
            return found[0]
        else:
            return None

    def is_blocked(self, x, y):
        return self.at(x, y, blocks_movement=True) is not None


class Object:

    def __init__(self, name=None, x=0, y=0,
                 avatar=None, color=None,
                 movable=True, blocks_movement=True,
                 max_hp=sys.maxint, hp=None,
                 offense=0, defense=0,
                 **kwargs):
        self.name = name

        self.x = x
        self.y = y
        self.movable = movable
        self.blocks_movement = blocks_movement

        self.avatar = avatar
        self.color = color

        self.max_hp = max_hp
        self.hp = hp or max_hp  # if unspecified, default to full life
        self.offense = offense
        self.defense = defense

    def calculate_destination(self, dx, dy):
        new_x = self.x
        new_y = self.y

        if self.movable:
            new_x += dx
            new_y += dy

        return new_x, new_y

    def move(self, dx, dy):
        if self.movable:
            self.x += dx
            self.y += dy

    def draw(self):
        context = get_context()
        context.console.put_map_char(self.avatar, self.x, self.y,
                                     fg_color=self.color)

    def clear(self):
        get_context().console.clear_map_char(self.x, self.y)
