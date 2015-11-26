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


class VentureConfig:

    def __init__(self):

        # General
        self.skin = DefaultSkin()

        # Screen & Map
        self.font_path = 'fonts/arial12x12.png'
        self.title = 'Venture Society'

        self.fps_limit = 20

        self.screen_width = 80
        self.screen_height = 60

        self.map_width = 80
        self.map_height = 55

        self.fov_algorithm = 0
        self.fov_light_walls = True

        # Map
        self.map_use_fog = True

        # Objects
        self.object_use_fov = True

        # Player
        self.player_avatar = '@'
        self.player_color = cod.Color(49, 192, 214)
        self.player_torch_radius = 10
        self.player_max_hp = 20
        self.player_offense = 5
        self.player_defense = 5

        # Mob
        self.mob_default_color = cod.Color(250, 120, 120)
        self.mob_max_per_room = 2


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
