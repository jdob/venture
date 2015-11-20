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

from venture.model.base import Object


class Mob(Object):

    def __init__(self, name, avatar, color, max_hp,
                 hp, offense, defense, **kwargs):
        Object.__init__(self, name=name,
                        avatar=avatar,
                        color=color,
                        max_hp=max_hp,
                        hp=hp,
                        offense=offense,
                        defense=defense)
