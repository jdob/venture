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

from venture.model.base import Combatant


class Mob(Combatant):

    def __init__(self, game, name, avatar, color, max_hp,
                 hp, offense, defense, **kwargs):
        Combatant.__init__(self,
                           game,
                           name=name,
                           avatar=avatar,
                           color=color,
                           max_hp=max_hp,
                           hp=hp,
                           offense=offense,
                           defense=defense)

    def take_turn(self):

        # Default behavior is to run at the player
        # if it can be seen
        if self.game.console.in_fov(self.x, self.y):

            # If there is still distance to cover, move
            if self.distance_to(self.game.player) >= 2:
                self.move_towards(self.game.player.x, self.game.player.y)

            else:
                print('Attacking!')
