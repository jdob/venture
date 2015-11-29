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


class Player(Combatant):

    def __init__(self, game):
        config = game.config
        Combatant.__init__(self,
                           game,
                           name='Player',  # for debug purposes
                           avatar=config.player_avatar,
                           color=config.player_color,
                           max_hp=config.player_max_hp,
                           offense=config.player_offense,
                           defense=config.player_defense)
