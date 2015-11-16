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
from venture.lib import libtcodpy as cod
from venture.maps.tomb import Tomb
from venture.model.base import Objects
from venture.model.player import Player

# Notifications from handle_keys
KEY_EXIT = 'exit'
KEY_FOV_RECOMPUTE = 'fov_recompute'


class VentureEngine:

    def __init__(self):
        self.context = context.get_context()
        self.config = self.context.config
        self.console = self.context.console

        self.objects = Objects()
        self.map = None
        self.player = None

    def initialize(self):

        self.map = Tomb(5, 4)
        self.map.generate()

        self.console.initialize()
        self.console.initialize_fov(self.map)

        self.player = Player()
        self.player.x, self.player.y = self.map.player_start_location()
        self.objects.append(self.player)

        # Mob sample generation
        from venture.model.mobs import place_sample_mobs
        added_mobs = place_sample_mobs(self.map.rooms)
        self.objects.extend(added_mobs)

    def run(self):

        fov_recompute = True
        while not cod.console_is_window_closed():

            self.draw_all(fov_recompute)
            self.context.console.blit_map()
            self.context.console.flush()

            for o in self.objects:
                o.clear()

            fov_recompute = False
            key_result = self.handle_keys()

            if key_result == KEY_EXIT:
                break
            elif key_result == KEY_FOV_RECOMPUTE:
                fov_recompute = True

    def handle_keys(self):

        # Configure for turn-based
        key = cod.console_wait_for_keypress(True)
     
        if key.vk == cod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            cod.console_set_fullscreen(not cod.console_is_fullscreen())
     
        elif key.vk == cod.KEY_ESCAPE:
            # Exit Game
            return KEY_EXIT
     
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
                return KEY_FOV_RECOMPUTE

    def draw_all(self, fov_recompute):
        self._draw_map(fov_recompute)
        self._draw_objects()

    def _draw_map(self, fov_recompute):
        if not fov_recompute:
            return

        self.console.compute_fov(self.player.x, self.player.y)

        for y in range(self.config.map_height):
            for x in range(self.config.map_width):
                in_fov = self.console.in_fov(x, y)
                is_wall = self.map[x][y].block_sight

                if not in_fov:
                    # If not in the current FOV, only draw if it's
                    # been explored
                    if self.map[x][y].explored or not self.config.map_use_fog:
                        if is_wall:
                            self.console.set_map_bg_color(self.config.wall_color_dark, x, y)
                        else:
                            self.console.set_map_bg_color(self.config.ground_color_dark, x, y)
                else:
                    self.map[x][y].explored = True

                    if is_wall:
                        self.console.set_map_bg_color(self.config.wall_color_light, x, y)
                    else:
                        self.console.set_map_bg_color(self.config.ground_color_light, x, y)

    def _draw_objects(self):
        for o in self.objects:
            o.draw()

    def _allow_move(self, new_x, new_y):
        return ((0 <= new_x < self.config.map_width) and
                (0 <= new_y < self.config.map_height) and
                not self.map[new_x][new_y].block_move and
                not self.objects.is_blocked(new_x, new_y)
               )
