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

import math
import sys


class Objects(list):

    def at(self, x, y, blocks_movement=False):
        found = [o for o in self if o.x == x and o.y == y]
        if blocks_movement:
            found = [o for o in found if o.blocks_movement]

        if len(found) > 1:
            raise Exception('Multiple objects [%s] found at (%s, %s)'
                            % (len(found), x, y))
        elif len(found) == 1:
            return found[0]
        else:
            return None

    def is_blocked(self, x, y):
        return self.at(x, y, blocks_movement=True) is not None


class Object(object):

    def __init__(self, game,
                 name=None, x=0, y=0,
                 avatar=None, color=None,
                 movable=True, blocks_movement=True,
                 **kwargs):
        self.game = game
        self.name = name

        self.x = x
        self.y = y
        self.movable = movable
        self.blocks_movement = blocks_movement

        self.avatar = avatar
        self.color = self.game.console.color(*color)

    def __str__(self):
        s = '%s, (%s,%s)'
        data = (self.name, self.x, self.y)
        return s % data

    def calculate_destination(self, dx, dy):
        new_x = self.x
        new_y = self.y

        if self.movable:
            new_x += dx
            new_y += dy

        return new_x, new_y

    def move(self, dx, dy):
        if self.movable:
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        dx, dy = self.calculate_move_towards(target_x, target_y)
        self.move(dx, dy)

    def calculate_move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        return dx, dy

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def draw(self):
        self.game.console.put_map_char(self.avatar, self.x, self.y,
                                       fg_color=self.color)

    def clear(self):
        self.game.console.clear_map_char(self.x, self.y)


class Combatant(Object):

    def __init__(self, game,
                 name=None, x=0, y=0, avatar=None, color=None,
                 movable=True, blocks_movement=True,
                 max_hp=sys.maxint, hp=None,
                 offense=0, defense=0,
                 **kwargs):
        super(Combatant, self).__init__(game, name, x, y, avatar, color,
                                        movable, blocks_movement, **kwargs)

        self.max_hp = max_hp
        self.hp = hp or max_hp   # if unspecified, default to full life
        self.offense = offense
        self.defense = defense

    def __str__(self):
        s = '%s, (%s,%s), %s/%s'
        data = (self.name, self.x, self.y, self.hp, self.max_hp)
        return s % data

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):

        # Hooks to allow combat to be modified
        self.pre_attack()
        target.pre_defend()

        damage = self.offense - target.defense

        if damage > 0:
            target.damage(damage)
            print('%s attacks %s for %s' % (self.name, target.name, damage))
        else:
            print('%s does no damage to %s' % (self.name, target.name))

        target.post_defend()
        self.post_attack()

    def damage(self, amount):
        self.hp -= amount

    def pre_attack(self):
        pass

    def post_attack(self):
        pass

    def pre_defend(self):
        pass

    def post_defend(self):
        pass

    def die(self):
        pass

