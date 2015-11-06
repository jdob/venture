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

from venture.lib import libtcodpy as cod


class VentureConsole:

    def __init__(self, config):
        self.config = config
        self.map_console = None
        self.fov_map = None

    def initialize(self):

        # Basic Configuration
        cod.console_set_custom_font(
            self.config.font_path,
            cod.FONT_TYPE_GREYSCALE | cod.FONT_LAYOUT_TCOD)
        cod.console_init_root(self.config.screen_width,
                              self.config.screen_height,
                              self.config.title,
                              fullscreen=False)
        cod.sys_set_fps(self.config.fps_limit)

        # Consoles
        self.map_console = cod.console_new(self.config.screen_width,
                                           self.config.screen_height)

    def initialize_fov(self, map):
        self.fov_map = cod.map_new(self.config.map_width, self.config.map_height)
        for y in range(self.config.map_height):
            for x in range(self.config.map_width):
                cod.map_set_properties(self.fov_map, x, y,
                                       not map[x][y].block_sight,
                                       not map[x][y].block_move)

    def put_map_char(self, char, x, y,
                     fg_color=cod.white, bg_color=cod.BKGND_NONE):
        cod.console_set_default_foreground(self.map_console,
                                           fg_color)
        cod.console_put_char(self.map_console, x, y, char, bg_color)

    def clear_map_char(self, x, y):
        cod.console_put_char(self.map_console, x, y, ' ', cod.BKGND_NONE)

    def blit_map(self):
        cod.console_blit(self.map_console, 0, 0,
                         self.config.screen_width,
                         self.config.screen_height, 0, 0, 0)

    def set_map_bg_color(self, color, x, y):
        cod.console_set_char_background(self.map_console, x, y,
                                        color, cod.BKGND_SET )

    def compute_fov(self, x, y):
        cod.map_compute_fov(self.fov_map, x, y,
                            self.config.torch_radius,
                            self.config.fov_light_walls,
                            self.config.fov_algorithm)

    def in_fov(self, x, y):
        return cod.map_is_in_fov(self.fov_map, x, y)

    @staticmethod
    def flush():
        cod.console_flush()
