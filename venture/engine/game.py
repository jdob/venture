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

from venture.engine.config import VentureConfig
from venture.engine.console import VentureConsole
from venture.maps.tomb import Tomb
from venture.mobs.simple import SimpleMobGenerator
from venture.model.base import Objects
from venture.model.player import Player


class Game:

    def __init__(self):
        self.config = None
        self.console = None

        self.objects = None
        self.map = None

        self.player = None
        self.mob_generator = None

    def initialize(self):
        self.config = VentureConfig()
        self.console = VentureConsole(self.config)

        self.objects = Objects()

        self.map = Tomb(self, 5, 4, 1)
        self.map.generate()

        self.console.initialize()
        self.console.initialize_fov(self.map)

        self.player = Player(self)
        self.player.x, self.player.y = self.map.player_start_location()
        self.objects.append(self.player)

        self.mob_generator = SimpleMobGenerator(self)
        added_mobs = self.mob_generator.add_mobs(self.map.rooms)
        self.objects.extend(added_mobs)


__GAME = Game()


def game():
    return __GAME
