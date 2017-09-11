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


class VentureConfig:

    def __init__(self):

        # General
        self.skin = DefaultSkin()

        # Screen
        self.font_path = 'fonts/arial12x12.png'
        self.title = 'Venture Society'
        self.fps_limit = 20

        # Consoles & Sizes
        self.map_width = 80
        self.map_height = 58

        self.status_width = 80
        self.status_height = 2

        self.screen_width = self.map_width
        self.screen_height = self.map_height + self.status_height

        self.fov_algorithm = 0
        self.fov_light_walls = True

        # Map
        self.map_use_fog = True

        # Objects
        self.object_use_fov = True

        # Player
        self.player_avatar = '@'
        self.player_color = (49, 192, 214)
        self.player_torch_radius = 10
        self.player_max_hp = 20
        self.player_offense = 5
        self.player_defense = 5

        # Mob
        self.mob_default_color = (250, 120, 120)
        self.mob_max_per_room = 0


class DefaultSkin:

    def __init__(self):

        self.wall_char = '#'
        self.wall_bg_dark = (20, 20, 20)
        self.wall_bg_light = self.wall_bg_dark
        self.wall_fg_dark = (150, 150, 150)
        self.wall_fg_light = (235, 235, 235)

        self.ground_char = '.'
        self.ground_bg_dark = (20, 20, 20)
        self.ground_bg_light = self.ground_bg_dark
        self.ground_fg_dark = (150, 150, 150)
        self.ground_fg_light = (235, 235, 235)

        self.status_bar_fg = (179, 198, 255)
        self.status_bar_bg = (25, 25, 25)
        # self.status_bar_bg = (179, 198, 255)
