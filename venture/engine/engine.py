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

from venture.engine import context
import venture.lib.libtcodpy as cod
from venture.model.base import Player
from venture.model import map

class VentureEngine:

    def __init__(self):
        self.context = context.get_context()
        self.config = self.context.config
        self.console = self.context.console

        self.objects = []
        self.map = None
        self.player = None

    def initialize(self):
        self.context.initialize()

        self.map = map.Tomb(7, 2)
        self.map.generate()

        self.player = Player()
        self.player.x, self.player.y = self.map.player_start_location()
        self.objects.append(self.player)

    def run(self):

        while not cod.console_is_window_closed():

            self.draw_all()
            self.context.console.blit_map()
            self.context.console.flush()

            for o in self.objects:
                o.clear()

            exit_triggered = self.handle_keys()
            if exit_triggered:
                break

    def handle_keys(self):

        # Configure for turn-based
        key = cod.console_wait_for_keypress(True)
     
        if key.vk == cod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            cod.console_set_fullscreen(not cod.console_is_fullscreen())
     
        elif key.vk == cod.KEY_ESCAPE:
            # Exit Game
            return True
     
        # Movement
        dx = dy = None
        if cod.console_is_key_pressed(cod.KEY_UP):
            dx = 0
            dy = -1

        elif cod.console_is_key_pressed(cod.KEY_DOWN):
            dx = 0
            dy = 1

        elif cod.console_is_key_pressed(cod.KEY_LEFT):
            dx = -1
            dy = 0

        elif cod.console_is_key_pressed(cod.KEY_RIGHT):
            dx = 1
            dy = 0

        if dx is not None:
            new_x, new_y = self.player.calculate_destination(dx, dy)

            if self._allow_move(new_x, new_y):
                self.player.move(dx, dy)

    def draw_all(self):
        # Draw all objects
        for o in self.objects:
            o.draw()

        # Draw the map
        for y in range(self.config.map_height):
            for x in range(self.config.map_width):
                is_wall = self.map[x][y].block_sight
                if is_wall:
                    self.console.set_map_bg_color(self.config.color_dark_wall, x, y)
                else:
                    self.console.set_map_bg_color(self.config.color_dark_ground, x, y)

    def _allow_move(self, new_x, new_y):
        return ((0 <= new_x < self.config.map_width) and
                (0 <= new_y < self.config.map_height) and
                not self.map[new_x][new_y].block_move)
