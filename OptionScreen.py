import sys
import pygame
from Screen import Screen


class OptionScreen(Screen):
    """The Screen that allows user to set the game options before playing. Can navigate to Game Screen from here."""

    cpu_opponent = False
    cpu_difficulty = 0
    cpu_x = False

    player_x_first = True

    def mouse_pos_player_1(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Player 1'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 22 < mouse_position[0] < 77 and 92 < mouse_position[1] < 108:
            return True
        else:
            return False

    def mouse_pos_player_2(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Player 2'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 22 < mouse_position[0] < 77 and 142 < mouse_position[1] < 158:
            return True
        else:
            return False

    def mouse_pos_human(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Human'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 124 < mouse_position[0] < 176 and 92 < mouse_position[1] < 108:
            return True
        else:
            return False

    def mouse_pos_computer(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Computer'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 113 < mouse_position[0] < 187 and 142 < mouse_position[1] < 158:
            return True
        else:
            return False

    def mouse_pos_easy(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Easy'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 252 < mouse_position[0] < 289 and 92 < mouse_position[1] < 108:
            return True
        else:
            return False

    def mouse_pos_medium(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Medium'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 241 < mouse_position[0] < 300 and 142 < mouse_position[1] < 158:
            return True
        else:
            return False

    def mouse_pos_hard(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Hard'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 251 < mouse_position[0] < 289 and 192 < mouse_position[1] < 208:
            return True
        else:
            return False

    def mouse_pos_player_x(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Player X'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 390 < mouse_position[0] < 450 and 92 < mouse_position[1] < 108:
            return True
        else:
            return False

    def mouse_pos_player_o(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Player O'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 390 < mouse_position[0] < 450 and 142 < mouse_position[1] < 158:
            return True
        else:
            return False

    def mouse_pos_start(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Start'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 217 < mouse_position[0] < 283 and 243 < mouse_position[1] < 272:
            return True
        else:
            return False

    def run_screen(self):
        """Runs the Option Screen.

        Checks for any events (mouse events, etc.) and does appropriate action.
        Displays any text or other images on the display.
        """
        while 1:
            self.display.fill(self.white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.conn.close()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()
                    if (
                            ((self.mouse_pos_player_1(mouse_position) or self.mouse_pos_player_2(mouse_position))
                                and not self.cpu_opponent)
                            or (self.mouse_pos_human(mouse_position) or self.mouse_pos_computer(mouse_position))
                            or ((self.mouse_pos_easy(mouse_position) or self.mouse_pos_medium(mouse_position)
                                 or self.mouse_pos_hard(mouse_position) or self.mouse_pos_player_x(mouse_position)
                                 or self.mouse_pos_player_o(mouse_position)) and self.cpu_opponent)
                            or (self.mouse_pos_start(mouse_position))
                    ):
                        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                    else:
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if self.mouse_pos_player_1(mouse_position) and not self.cpu_opponent:
                        self.player_x_first = True
                    elif self.mouse_pos_player_2(mouse_position) and not self.cpu_opponent:
                        self.player_x_first = False
                    elif self.mouse_pos_human(mouse_position):
                        self.cpu_opponent = False
                    elif self.mouse_pos_computer(mouse_position):
                        self.cpu_opponent = True
                    elif self.mouse_pos_easy(mouse_position) and self.cpu_opponent:
                        self.cpu_difficulty = 0
                    elif self.mouse_pos_medium(mouse_position) and self.cpu_opponent:
                        self.cpu_difficulty = 1
                    elif self.mouse_pos_hard(mouse_position) and self.cpu_opponent:
                        self.cpu_difficulty = 2
                    elif self.mouse_pos_player_x(mouse_position) and self.cpu_opponent:
                        self.cpu_x = True
                    elif self.mouse_pos_player_o(mouse_position) and self.cpu_opponent:
                        self.cpu_x = False
                    elif self.mouse_pos_start(mouse_position):
                        from GameScreen import GameScreen
                        g = GameScreen()
                        g.init(self.player_x_first, self.cpu_opponent, self.cpu_difficulty, self.cpu_x)

            self.display_message("First Player", 50, 50, 14)
            if not self.cpu_opponent:
                if self.player_x_first:
                    self.display_message("Player 1", 50, 100, 14, self.red)
                    self.display_message("Player 2", 50, 150, 14)
                else:
                    self.display_message("Player 1", 50, 100, 14)
                    self.display_message("Player 2", 50, 150, 14, self.red)
            else:
                self.display_message("Player 1", 50, 100, 14, self.gray)
                self.display_message("Player 2", 50, 150, 14, self.gray)

            self.display_message("Opponent", 150, 50, 14)
            if self.cpu_opponent:
                self.display_message("Human", 150, 100, 14)
                self.display_message("Computer", 150, 150, 14, self.red)
            else:
                self.display_message("Human", 150, 100, 14, self.red)
                self.display_message("Computer", 150, 150, 14)

            self.display_message("Computer Difficulty", 270, 50, 14)
            if self.cpu_opponent:
                if self.cpu_difficulty == 0:
                    self.display_message("Easy", 270, 100, 14, self.red)
                    self.display_message("Medium", 270, 150, 14)
                    self.display_message("Hard", 270, 200, 14)
                elif self.cpu_difficulty == 1:
                    self.display_message("Easy", 270, 100, 14)
                    self.display_message("Medium", 270, 150, 14, self.red)
                    self.display_message("Hard", 270, 200, 14)
                elif self.cpu_difficulty == 2:
                    self.display_message("Easy", 270, 100, 14)
                    self.display_message("Medium", 270, 150, 14)
                    self.display_message("Hard", 270, 200, 14, self.red)
            else:
                self.display_message("Easy", 270, 100, 14, self.gray)
                self.display_message("Medium", 270, 150, 14, self.gray)
                self.display_message("Hard", 270, 200, 14, self.gray)

            self.display_message("Computer Character", 420, 50, 14)
            if self.cpu_opponent:
                if self.cpu_x:
                    self.display_message("Player X", 420, 100, 14, self.red)
                    self.display_message("Player O", 420, 150, 14)
                else:
                    self.display_message("Player X", 420, 100, 14)
                    self.display_message("Player O", 420, 150, 14, self.red)
            else:
                self.display_message("Player X", 420, 100, 14, self.gray)
                self.display_message("Player O", 420, 150, 14, self.gray)

            self.display_message("Start", 250, 260, 26)

            pygame.display.flip()
