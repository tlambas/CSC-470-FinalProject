import sys
import pygame
from Screen import Screen


class RecordScreen(Screen):
    """The Screen that shows the user the previous game records. Can delete all records or
    navigate back to Start Screen from here.
    """

    messages_displayed = False
    curs = None
    records = None
    row_heights = None

    def mouse_pos_start(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Start Screen'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 70 < mouse_position[0] < 230 and 260 < mouse_position[1] < 286:
            return True
        else:
            return False

    def mouse_pos_reset(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Reset'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 315 < mouse_position[0] < 385 and 260 < mouse_position[1] < 286:
            return True
        else:
            return False

    def get_records(self):
        """Gets the rows from the database table and sets the information in the records variable"""
        self.curs = self.conn.execute('''
        SELECT * FROM records
        ORDER BY date DESC
        LIMIT 10
            ''')
        self.conn.commit()
        self.records = self.curs.fetchall()

    def reset_records(self):
        """Deletes all information from the database table"""
        self.conn.execute('''
        DELETE FROM records
            ''')
        self.conn.commit()

    def run_screen(self):
        """Runs the Record Screen.

        Checks for any events (mouse events, etc.) and does appropriate action.
        Displays any text or other images on the display.
        """
        self.create_table()
        self.get_records()

        while 1:
            height = 50
            self.display.fill(self.white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.conn.close()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()
                    if self.mouse_pos_start(mouse_position) or self.mouse_pos_reset(mouse_position):
                        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                    else:
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if self.mouse_pos_start(mouse_position):
                        from StartScreen import StartScreen
                        s = StartScreen()
                        s.init()
                    elif self.mouse_pos_reset(mouse_position):
                        self.reset_records()
                        self.get_records()

            self.display_message("Date", 76, 20, 15)
            self.display_message("Winner", 187, 20, 15)
            self.display_message("Character", 270, 20, 15)
            self.display_message("Total Turns", 362, 20, 15)
            self.display_message("Difficulty", 450, 20, 15)
            pygame.draw.line(self.display, self.black, (10, 30), (490, 30), 2)

            for row in self.records:
                self.display_message(row[0], 76, height)
                self.display_message(row[1], 187, height)
                self.display_message(row[2], 270, height)
                self.display_message(str(row[3]), 362, height)
                self.display_message(row[4], 450, height)
                height = height + 20

            self.display_message("Start Screen", 150, 275, 26)
            self.display_message("Reset", 350, 275, 26)

            pygame.display.flip()



