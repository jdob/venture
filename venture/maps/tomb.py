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

from venture.engine.context import get_context
from venture.maps.base import (Map, Room)


class Tomb(Map):

    def __init__(self, grid_size, corridor_length,
                 iterable=None, **kwargs):
        super(Tomb, self).__init__(iterable, **kwargs)

        # Number of rooms in each row and column
        self.grid_size = grid_size
        self.corridor_length = corridor_length

    def generate(self):
        super(Tomb, self).generate()

        # TODO: Add validation on number feasibility

        rooms = self._generate_rooms()
        self._generate_corridors(rooms)

    def _generate_rooms(self):
        room_size, total_size = self._calculate_room_size()
        pad_x, pad_y = self._calculate_padding(total_size)

        rooms = []
        x = pad_x
        y = pad_y

        for i in range(self.grid_size):

            # Create all rooms in the current column (x)
            for j in range(self.grid_size):
                r = Room(x, y, room_size, room_size)
                rooms.append(r)
                y = y + room_size + self.corridor_length

            # Increment to the next column
            x = x + room_size + self.corridor_length

            # Reset to the top row
            y = pad_y

        for r in rooms:
            self.create_room(r)

        return rooms

    def _generate_corridors(self, rooms):

        # Vertical Corridors
        for index, r in enumerate(rooms):

            # Skip the last room in each column
            if (index + 1) % self.grid_size == 0:
                continue

            # Center the corridor as best as possible
            x = (r.x1 + r.x2) / 2
            y1 = r.y2  # start at the bottom of the room
            y2 = y1 + self.corridor_length
            self.create_vertical_tunnel(y1, y2, x)

        # Horizontal Corridors
        for i in range(self.grid_size * (self.grid_size - 1)):
            r = rooms[i]
            y = (r.y1 + r.y2) / 2
            x1 = r.x2
            x2 = x1 + self.corridor_length
            self.create_horizontal_tunnel(x1, x2, y)

    def _calculate_room_size(self):
        """Based on the map size and number of rooms, determines the
        largest size each room can be. Only odd number length rooms will
        be used to make the corridor connections look better.

        :return: size of each room, sum of all rooms and corridors
        :rtype: int, int
        """
        config = get_context().config

        short_side = min(config.map_height, config.map_width)

        largest_room_size = 0
        total_size = 0
        total_corridor_len = self.corridor_length * (self.grid_size - 1)
        for check_size in range(3, short_side, 2):
            all_rooms_len = check_size * self.grid_size
            rooms_and_corridors = all_rooms_len + total_corridor_len
            if rooms_and_corridors <= short_side:
                largest_room_size = check_size
                total_size = rooms_and_corridors
            else:
                break

        return largest_room_size, total_size

    @staticmethod
    def _calculate_padding(total_size):
        config = get_context().config
        pad_x = (config.map_width - total_size) / 2
        pad_y = (config.map_height - total_size) / 2
        return pad_x, pad_y
