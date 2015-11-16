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

        # Map Colors
        self.color_dark_wall = cod.Color(0, 0, 100)
        self.color_light_wall = cod.Color(130, 110, 50)
        self.color_dark_ground = cod.Color(50, 50, 150)
        self.color_light_ground = cod.Color(200, 180, 50)

        # Player
        self.player_avatar = '@'
        self.player_color = cod.light_cyan
        self.torch_radius = 10

        # Mob
        self.mob_default_color = cod.light_red

        # Debug
        self.use_fog = True


