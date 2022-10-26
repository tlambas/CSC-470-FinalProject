import pygame
import sqlite3


class Screen:
    """The base Screen class.

    This class will contain all of the basic information for the any additional Screens that may inherit from it.
    This information includes variables and methods that could be used by any Screen.
    """

    size = width, height = 500, 300
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0
    gray = 128, 128, 128

    display = pygame.display.set_mode(size)

    DB_FILENAME = 'records.db'
    conn = sqlite3.connect(DB_FILENAME)

    def __init__(self):
        self.size = 500, 300
        self.black = 0, 0, 0
        self.white = 255, 255, 255
        self.red = 255, 0, 0
        self.gray = 128, 128, 128

        self.display = pygame.display.set_mode(self.size)

    def display_message(self, text, pos_x, pos_y, size=14, color=black):
        """Creates a text image on the Screen.

        Keyword arguments:
        text -- the text to be displayed
        pos_x -- the X position for the center of the text image
        pos_y -- the Y position for the center of the text image
        size -- the font size (default 14)
        color -- the text's color (default black)
        """
        text_font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = text_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        self.display.blit(text_surface, text_rect)

    def create_table(self):
        """Creates a database table to store game records."""
        curs = self.conn.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='records'
            ''')
        if len(curs.fetchall()) < 1:
            self.conn.execute('''
            CREATE TABLE records (date text, player text, character text, turns integer, difficulty text)
            ''')
        self.conn.commit()

    def init(self):
        """Initializes the current Screen"""
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.run_screen()

    def run_screen(self):
        """Runs the current Screen. Will need to have logic in inherited Screens."""
        pass
