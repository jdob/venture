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

import random

from venture.engine.game import game
from venture.mobs import data
from venture.model.mobs import Mob


class SimpleMobGenerator:
    """
    Adds a random (up to a limit) number of mobs per room.
    """

    def add_mobs(self, rooms):
        config = game().config

        added_mobs = []
        for room in rooms:
            num_mobs = random.randint(0, config.mob_max_per_room)

            for i in range(num_mobs):
                # Random location for the mob
                x = random.randint(room.x1, room.x2 - 1)
                y = random.randint(room.y1, room.y2 - 1)

                mob_type = data.random_mob()
                mob = Mob(**mob_type)

                mob.x = x
                mob.y = y
                added_mobs.append(mob)

        return added_mobs
