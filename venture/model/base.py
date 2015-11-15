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

from venture.engine.context import get_context


class Object:

    def __init__(self, avatar=None, color=None):
        self.x = 0
        self.y = 0
        self.movable = True

        self.avatar = avatar
        self.color = color

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
