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
        self.fov_map = None

        self.map_console = None
        self.status_console = None
        self.details_console = None

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
        self.map_console = cod.console_new(self.config.map_width,
                                           self.config.map_height)
        self.status_console = cod.console_new(self.config.status_width,
                                              self.config.status_height)
        self.details_console = cod.console_new(self.config.details_width,
                                               self.config.details_height)

    def initialize_fov(self, f_map):
        self.fov_map = cod.map_new(self.config.map_width, self.config.map_height)
        for y in range(self.config.map_height):
            for x in range(self.config.map_width):
                cod.map_set_properties(self.fov_map, x, y,
                                       not f_map[x][y].block_sight,
                                       not f_map[x][y].block_move)

    def put_map_char(self, char, x, y,
                     fg_color=cod.white, bg_color=cod.BKGND_NONE):
        cod.console_set_default_foreground(self.map_console, fg_color)
        cod.console_put_char(self.map_console, x, y, char, bg_color)

    def clear_map_char(self, x, y):
        cod.console_put_char(self.map_console, x, y, ' ', cod.BKGND_NONE)

    def blit_map(self):
        cod.console_blit(self.map_console, 0, 0,
                         self.config.screen_width,
                         self.config.screen_height, 0, 0, 0)

    def set_map_bg_color(self, color, x, y):
        cod.console_set_char_background(self.map_console, x, y,
                                        color, cod.BKGND_SET)

    def compute_fov(self, x, y):
        cod.map_compute_fov(self.fov_map, x, y,
                            self.config.player_torch_radius,
                            self.config.fov_light_walls,
                            self.config.fov_algorithm)

    def in_fov(self, x, y):
        return cod.map_is_in_fov(self.fov_map, x, y)

    def render_status_bar(self, text):
        # Clear the previous contents of the console (otherwise the colors
        # get all weird)
        cod.console_clear(self.status_console)

        # Set the rendering colors for the status bar
        cod.console_set_default_foreground(
            self.status_console,
            self.color(*self.config.skin.status_bar_fg))
        # cod.console_set_default_background(
        #     self.status_console,
        #     self.color(*self.config.skin.status_bar_bg))

        # The following code will eventually be used for a graphical HP bar
        # to render the background (total health).
        # cod.console_rect(self.status_console, 0, 0, self.config.status_width,
        #                  self.config.status_height, False, cod.BKGND_SCREEN)

        # Print the status bar text to the screen
        #   The following will center the text
        # cod.console_print_ex(self.status_console,
        #                      self.config.status_width / 2, 0,
        #                      cod.BKGND_NONE, cod.CENTER,
        #                      text)
        cod.console_print_ex(self.status_console,
                             1, 0,
                             cod.BKGND_NONE, cod.LEFT,
                             text)

    def blit_status_bar(self):
        bar_y = self.config.screen_height - self.config.status_height
        cod.console_blit(self.status_console, 0, 0,
                         self.config.status_width,
                         self.config.status_height, 0,
                         0, bar_y)

    def render_details(self, text):
        cod.console_clear(self.details_console)
        cod.console_set_default_foreground(
            self.details_console,
            self.color(*self.config.skin.details_fg)
        )
        cod.console_print_ex(self.details_console,
                             1, 0,
                             cod.BKGND_NONE, cod.LEFT,
                             text)

    def blit_details(self):
        # Place to the right of the status bar, with a small gap
        details_x = self.config.status_width + 2
        details_y = self.config.screen_height - self.config.status_height
        cod.console_blit(self.details_console, 0, 0,
                         self.config.details_width,
                         self.config.details_height, 0,
                         details_x, details_y)

    @staticmethod
    def color(r, g, b):
        return cod.Color(r, g, b)

    @staticmethod
    def flush():
        cod.console_flush()
