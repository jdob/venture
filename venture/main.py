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

import argparse

from venture.engine.engine import VentureEngine
from venture.engine.context import get_context


def main():
    _parse_args()

    engine = VentureEngine()
    engine.initialize()
    engine.run()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-fog', dest='no_fog', action='store_true')
    parser.add_argument('--no-fov', dest='no_fov', action='store_true')

    args = parser.parse_args()
    args = vars(args)

    config = get_context().config
    config.map_use_fog = not args['no_fog']
    config.object_use_fov = not args['no_fov']


if __name__ == '__main__':
    main()
