import sys
import pygame
from Screen import Screen


class StartScreen(Screen):
    """The Screen to be shown at the start of the game. Can navigate to Option Screen or Record Screen from here."""

    def mouse_pos_start(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Start'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 120 < mouse_position[0] < 180 and 137 < mouse_position[1] < 160:
            return True
        else:
            return False

    def mouse_pos_records(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Records'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 300 < mouse_position[0] < 400 and 137 < mouse_position[1] < 160:
            return True
        else:
            return False

    def run_screen(self):
        """Runs the Start Screen.

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
                    if self.mouse_pos_start(mouse_position) or self.mouse_pos_records(mouse_position):
                        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                    else:
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if self.mouse_pos_start(mouse_position):
                        from OptionScreen import OptionScreen
                        o = OptionScreen()
                        o.init()
                    elif self.mouse_pos_records(mouse_position):
                        from RecordScreen import RecordScreen
                        r = RecordScreen()
                        r.init()

            self.display_message("TIC-TAC-TOE", 250, 50, 50)
            self.display_message("Start", 150, 150, 25)
            self.display_message("Records", 350, 150, 25)

            pygame.display.flip()
