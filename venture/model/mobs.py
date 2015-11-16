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

from venture.engine.context import get_context
from venture.model.base import Object


def place_sample_mobs(rooms):
    # Purely for testing purposes (pretty obvious from the name)

    config = get_context().config

    orc = {
        'avatar': 'o',
        'color': config.mob_default_color
    }
    goblin = {
        'avatar': 'g',
        'color': config.mob_default_color
    }

    added_mobs = []
    for room in rooms:
        num_mobs = random.randint(0, config.mob_max_per_room)

        for i in range(num_mobs):
            # Random location for the mob
            x = random.randint(room.x1, room.x2 - 1)
            y = random.randint(room.y1, room.y2 - 1)

            mob_type = random.randint(1, 100)
            if mob_type <= 80:
                mob = Mob(**goblin)
            else:
                mob = Mob(**orc)

            mob.x = x
            mob.y = y
            added_mobs.append(mob)

    return added_mobs




class Mob(Object):

    def __init__(self, avatar, color):
        Object.__init__(self, avatar=avatar, color=color)
