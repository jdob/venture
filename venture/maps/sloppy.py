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
from venture.model.map import Map, Room


class SloppyDungeon(Map):

    def __init__(self, room_min_size, room_max_size, max_rooms,
                 iterable=None, **kwargs):
        super(SloppyDungeon, self).__init__(iterable, **kwargs)

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.max_rooms = max_rooms

    def generate(self):
        super(SloppyDungeon, self).generate()
        config = get_context().config

        rooms = []
        num_rooms = 0

        for r in range(self.max_rooms):
            w = random.randint(self.room_min_size, self.room_max_size)
            h = random.randint(self.room_min_size, self.room_max_size)

            x = random.randint(0, config.map_width - w - 1)
            y = random.randint(0, config.map_height - h - 1)

            new_room = Room(x, y, w, h)

            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                self.create_room(new_room)

                if num_rooms > 0:
                    new_x, new_y = new_room.center()
                    prev_x, prev_y = rooms[num_rooms-1].center()

                    if random.randint(0, 1) == 1:
                        self.create_horizontal_tunnel(prev_x, new_x, prev_y)
                        self.create_vertical_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_vertical_tunnel(prev_y, new_y, prev_x)
                        self.create_horizontal_tunnel(prev_x, new_x, new_y)

                rooms.append(new_room)
                num_rooms += 1
