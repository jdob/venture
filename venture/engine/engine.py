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

from venture.engine import game
from venture.lib import libtcodpy as cod


class VentureEngine:

    def __init__(self):

        # These variables left in place to speed along porting
        # all of these values into Game. There shouldn't be an
        # issue (just looks a bit weird) and will make accessing
        # them a bit cleaner.
        self.game = game.game()
        self.config = self.game.config
        self.console = self.game.console

        self.objects = self.game.objects
        self.map = self.game.map
        self.player = self.game.player
        self.mob_generator = self.game.mob_generator

    def run(self):

        fov_recompute = True
        while self._is_running():

            self._draw_all(fov_recompute)
            self.game.console.blit_map()
            self.game.console.flush()

            for o in self.objects:
                o.clear()

            # Player Turn
            fov_recompute = False
            key_result = self._handle_key()

            if key_result.end_game:
                break
            elif key_result.fov_recompute:
                fov_recompute = True
            elif key_result.bumped_object is not None:
                o = key_result.bumped_object
                print('Bumped into %s' % o)

            # Mobs turn (if the player made its move)
            if key_result.player_turn_finished:
                self._activate_mobs()


    @staticmethod
    def _is_running():
        return not cod.console_is_window_closed()

    def _handle_key(self):

        # Configure for turn-based
        key = cod.console_wait_for_keypress(True)
        key_char = chr(key.c)

        # Alt+Enter: toggle fullscreen
        if key.vk == cod.KEY_ENTER and key.lalt:
            cod.console_set_fullscreen(not cod.console_is_fullscreen())
            return KeyResult()

        # Exit Game
        elif key_char == 'q':
            return KeyResult(end_game=True)
     
        # Movement
        dx = dy = None
        if cod.console_is_key_pressed(cod.KEY_UP) or key_char == 'k':
            dx = 0
            dy = -1
        elif cod.console_is_key_pressed(cod.KEY_DOWN) or key_char == 'j':
            dx = 0
            dy = 1
        elif cod.console_is_key_pressed(cod.KEY_LEFT) or key_char == 'h':
            dx = -1
            dy = 0
        elif cod.console_is_key_pressed(cod.KEY_RIGHT) or key_char == 'l':
            dx = 1
            dy = 0
        elif key_char == 'y':
            dx = -1
            dy = -1
        elif key_char == 'u':
            dx = 1
            dy = -1
        elif key_char == 'b':
            dx = -1
            dy = 1
        elif key_char == 'n':
            dx = 1
            dy = 1

        if dx is not None:
            return self._handle_player_move_or_attack(dx, dy)

        # Unbound key pressed
        return KeyResult()

    def _handle_player_move_or_attack(self, dx, dy):
        """
        Handles a user input to attempt to move the player. This method
        will determine if the change to coordinates are a valid movement
        or if an attack takes place.

        :param dx: attempted change in the x plane
        :type  dx: int
        :param dy: attempted change in the y plane
        :type  dy: int
        :return: result describing the effects of the change
        :rtype:  KeyResult
        """
        new_x, new_y = self.player.calculate_destination(dx, dy)

        # First see if there is a mob at the destination
        mob = self.objects.at(new_x, new_y)
        if mob is not None:
            return KeyResult(player_turn_finished=True, bumped_object=mob)

        # If the player didn't bump into a mob, see if the move is valid
        # with respect to the map
        if self._allow_move(new_x, new_y):
            self.player.move(dx, dy)
            return KeyResult(player_turn_finished=True, fov_recompute=True)
        else:
            # No valid movement, so no need to recompute FOV
            return KeyResult()

    def _activate_mobs(self):
        mobs = [o for o in self.game.objects if o != self.game.player]
        for m in mobs:
            m.take_turn()

    def _allow_move(self, new_x, new_y):
        return ((0 <= new_x < self.config.map_width) and
                (0 <= new_y < self.config.map_height) and
                not self.map[new_x][new_y].block_move and
                not self.objects.is_blocked(new_x, new_y)
               )

    def _draw_all(self, fov_recompute):
        self._draw_map(fov_recompute)
        self._draw_objects()

    def _draw_map(self, fov_recompute):
        if not fov_recompute:
            return

        self.console.compute_fov(self.player.x, self.player.y)

        for y in range(self.config.map_height):
            for x in range(self.config.map_width):
                in_fov = self.console.in_fov(x, y)
                is_wall = self.map[x][y].block_sight

                bg_color = None
                fg_color = None
                char = None

                if not in_fov:
                    # If not in the current FOV, only draw if it's
                    # been explored
                    if self.map[x][y].explored or not self.config.map_use_fog:
                        if is_wall:
                            bg_color = self.console.color(*self.config.skin.wall_bg_dark)
                            fg_color = self.console.color(*self.config.skin.wall_fg_dark)
                            char = self.config.skin.wall_char
                        else:
                            bg_color = self.console.color(*self.config.skin.ground_bg_dark)
                            fg_color = self.console.color(*self.config.skin.ground_fg_dark)
                            char = self.config.skin.ground_char
                else:
                    self.map[x][y].explored = True

                    if is_wall:
                        bg_color = self.console.color(*self.config.skin.wall_bg_light)
                        fg_color = self.console.color(*self.config.skin.wall_fg_light)
                        char = self.config.skin.wall_char
                    else:
                        bg_color = self.console.color(*self.config.skin.ground_bg_light)
                        fg_color = self.console.color(*self.config.skin.ground_fg_light)
                        char = self.config.skin.ground_char

                if char is not None:
                    self.console.set_map_bg_color(bg_color, x, y)
                    self.console.put_map_char(char, x, y,
                                              fg_color=fg_color)

    def _draw_objects(self):
        for o in self.objects:
            in_fov = self.console.in_fov(o.x, o.y)
            if in_fov or not self.config.object_use_fov:
                o.draw()


class KeyResult:
    """
    Carries all of the metadata about the result of a user keypress.
    """

    def __init__(self,
                 player_turn_finished=False,
                 bumped_object=None,
                 end_game=False,
                 fov_recompute=False):
        self.player_turn_finished = player_turn_finished
        self.bumped_object = bumped_object
        self.end_game = end_game
        self.fov_recompute = fov_recompute
