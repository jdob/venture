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

import unittest

from venture.engine.game import game
from venture.model.base import Objects, Object


class ObjectsTests(unittest.TestCase):

    def setUp(self):
        super(ObjectsTests, self).setUp()
        self.game = game()
        self.game.initialize()
        self.objects = Objects()

    def test_at_found(self):
        # Setup
        self.objects.append(Object(self.game, name='yes', x=0, y=0))
        self.objects.append(Object(self.game, name='no', x=1, y=0))
        self.objects.append(Object(self.game, name='no', x=0, y=1))

        # Test
        found = self.objects.at(0, 0)

        # Verify
        self.assertTrue(found is not None)
        self.assertEqual('yes', found.name)

    def test_at_not_found(self):
        # Setup
        self.objects.append(Object(self.game, name='yes', x=0, y=0))
        self.objects.append(Object(self.game, name='no', x=1, y=0))
        self.objects.append(Object(self.game, name='no', x=0, y=1))

        # Test
        found = self.objects.at(10, 10)

        # Verify
        self.assertTrue(found is None)

    def test_at_multiple(self):
        # Setup
        self.objects.append(Object(self.game, name='first', x=0, y=0))
        self.objects.append(Object(self.game, name='second', x=0, y=0))
        self.objects.append(Object(self.game, name='no', x=0, y=1))

        # Test
        found = self.objects.at(0, 0)

        # Verify
        self.assertTrue(found is not None)
        self.assertEqual('first', found.name)
