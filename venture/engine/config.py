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
        self.wall_color_dark = cod.Color(164, 164, 164)
        self.wall_color_light = cod.Color(176, 176, 176)
        self.ground_color_dark = cod.Color(186, 186, 186)
        self.ground_color_light = cod.Color(196, 196, 196)

        # Player
        self.player_avatar = '@'
        self.player_color = cod.Color(43, 150, 186)
        self.player_torch_radius = 10

        # Mob
        self.mob_default_color = cod.Color(186, 62, 43)
        self.mob_max_per_room = 3

        # Debug
        self.use_fog = False


