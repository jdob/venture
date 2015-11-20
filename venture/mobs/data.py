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


_TEMPLATE = {
    'name': 'UNKNOWN',
    'avatar': 'X',
    'color': get_context().config.mob_default_color,
    'weight': 5,
    'max_hp': 10,
    'offense': 1,
    'defense': 1,
}

def _define(delta):
    x = dict(_TEMPLATE)
    x.update(delta)
    return x


ORC = _define({
    'name': 'Orc',
    'avatar': 'o',
    'weight': 2,
    'max_hp': 15,
    'offense': 3,
    'defense': 5,
})


GOBLIN = _define({
    'name': 'Goblin',
    'avatar': 'g',
    'offense': 2,
    'defense': 2,
})


KOBOLD = _define({
    'name': 'Kobold',
    'avatar': 'k',
    'weight': 7,
})


ALL = (ORC, GOBLIN, KOBOLD)


WEIGHTED_ALL = []
for m in ALL:
    WEIGHTED_ALL.extend([m] * m['weight'])


def random_mob():
    index = random.randint(0, len(WEIGHTED_ALL) - 1)
    mob = dict(WEIGHTED_ALL[index])

    # This may not belong here and instead in the generator, but this is
    # ok for now. Eventually I need to tweak the current HP as well to be
    # proportional to the max_hp (and maybe defense).
    mob['hp'] = mob['max_hp'] - random.randint(0, 2)
    return mob
