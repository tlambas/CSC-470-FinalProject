import sys
import pygame
from datetime import datetime
import time
import random
from Screen import Screen


class GameScreen(Screen):
    """The Screen which has the actual gameplay. Can navigate to Start Screen or Record Screen from here."""

    cpu_opponent = False
    cpu_difficulty = 0
    cpu_x = False
    cpu_turn = False

    player_1_first = True

    grid_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    player_1_turn = True
    game_over = 0
    game_saved = False

    clock = pygame.time.Clock()

    def init(self, player_1_first, cpu_opponent, cpu_difficulty, cpu_x):
        """Initializes the Game Screen.

        Keyword arguments:
        player_1_first -- whether or not Player 1 goes first
        cpu_opponent -- whether the user is facing a human or computer-controlled opponent
        cpu_difficulty -- how difficult the computer-controlled opponent will be to beat
        cpu_x -- whether or not the computer-controlled opponent goes first
        """
        self.player_1_first = player_1_first
        self.cpu_opponent = cpu_opponent
        self.cpu_difficulty = cpu_difficulty
        self.cpu_x = cpu_x
        if player_1_first:
            self.player_1_turn = True
            if cpu_x:
                self.cpu_turn = True
            else:
                self.cpu_turn = False
        else:
            self.player_1_turn = False

        self.grid_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.game_over = 0
        self.game_saved = False

        super().init()

    def cpu_take_turn(self):
        """Allows the computer-controlled opponent to decide which grid square to play."""
        time.sleep(1.5)

        if self.cpu_x:
            cpu_char = 1
        else:
            cpu_char = 2

        if self.cpu_difficulty == 0:
            self.cpu_take_turn_easy(cpu_char)
        elif self.cpu_difficulty == 1:
            self.cpu_take_turn_medium(cpu_char)
        elif self.cpu_difficulty == 2:
            self.cpu_take_turn_hard(cpu_char)

        self.cpu_turn = not self.cpu_turn
        self.player_1_turn = not self.player_1_turn

    def cpu_take_turn_easy(self, cpu_char):
        """Decides which grid square to play. Easy chooses a random empty square.

        Keyword arguments:
        cpu_char -- which character the computer-controlled opponent plays ('X' or 'O')
        """
        took_turn = False
        grid_choice = random.randint(0, 8)
        while not took_turn:
            if self.grid_state[grid_choice] == 0:
                self.grid_state[grid_choice] = cpu_char
                took_turn = True
            else:
                grid_choice = random.randint(0, 8)

    def cpu_take_turn_medium(self, cpu_char):
        """Decides which grid square to play. Medium tries to get three in a row or resorts to Easy.

        Keyword arguments:
        cpu_char -- which character the computer-controlled opponent plays ('X' or 'O')
        """
        grid_choice = self.find_two(cpu_char)
        if grid_choice >= 0:
            self.grid_state[grid_choice] = cpu_char
        else:
            grid_choice = self.find_one(cpu_char)
            if grid_choice >= 0:
                self.grid_state[grid_choice] = cpu_char
            else:
                if self.grid_state[4] == 0:
                    self.grid_state[4] = cpu_char
                else:
                    self.cpu_take_turn_easy(cpu_char)

    def cpu_take_turn_hard(self, cpu_char):
        """Decides which grid square to play. Hard tries to block opponent, then get three in a row, then resorts to
        Easy.

        Keyword arguments:
        cpu_char -- which character the computer-controlled opponent plays ('X' or 'O')
        """
        grid_choice = self.find_two(cpu_char)
        if grid_choice >= 0:
            self.grid_state[grid_choice] = cpu_char
        else:
            grid_choice = self.block_two(cpu_char)
            if grid_choice >= 0:
                self.grid_state[grid_choice] = cpu_char
            else:
                grid_choice = self.find_one(cpu_char)
                if grid_choice >= 0:
                    self.grid_state[grid_choice] = cpu_char
                else:
                    if self.grid_state[4] == 0:
                        self.grid_state[4] = cpu_char
                    else:
                        self.cpu_take_turn_easy(cpu_char)

    def find_two(self, cpu_char):
        """Allows the computer-controlled opponent to find two squares with the same character.

        Keyword arguments:
        cpu_char -- which character the computer-controlled opponent plays ('X' or 'O')
        """
        winning_spaces = []
        winning_choice = -1

        if (
                self.grid_state[1] == cpu_char and self.grid_state[2] == cpu_char and self.grid_state[0] == 0
                or self.grid_state[3] == cpu_char and self.grid_state[6] == cpu_char and self.grid_state[0] == 0
                or self.grid_state[4] == cpu_char and self.grid_state[8] == cpu_char and self.grid_state[0] == 0
        ):
            winning_spaces.append(0)
        if (
                self.grid_state[0] == cpu_char and self.grid_state[2] == cpu_char and self.grid_state[1] == 0
                or self.grid_state[4] == cpu_char and self.grid_state[7] == cpu_char and self.grid_state[1] == 0
        ):
            winning_spaces.append(1)
        if (
                self.grid_state[0] == cpu_char and self.grid_state[1] == cpu_char and self.grid_state[2] == 0
                or self.grid_state[5] == cpu_char and self.grid_state[8] == cpu_char and self.grid_state[2] == 0
                or self.grid_state[4] == cpu_char and self.grid_state[6] == cpu_char and self.grid_state[2] == 0
        ):
            winning_spaces.append(2)
        if (
                self.grid_state[4] == cpu_char and self.grid_state[5] == cpu_char and self.grid_state[3] == 0
                or self.grid_state[0] == cpu_char and self.grid_state[6] == cpu_char and self.grid_state[3] == 0
        ):
            winning_spaces.append(3)
        if (
                self.grid_state[3] == cpu_char and self.grid_state[5] == cpu_char and self.grid_state[4] == 0
                or self.grid_state[1] == cpu_char and self.grid_state[7] == cpu_char and self.grid_state[4] == 0
                or self.grid_state[0] == cpu_char and self.grid_state[8] == cpu_char and self.grid_state[4] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[6] == cpu_char and self.grid_state[4] == 0
        ):
            winning_spaces.append(4)
        if (
                self.grid_state[3] == cpu_char and self.grid_state[4] == cpu_char and self.grid_state[5] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[8] == cpu_char and self.grid_state[5] == 0
        ):
            winning_spaces.append(5)
        if (
                self.grid_state[7] == cpu_char and self.grid_state[8] == cpu_char and self.grid_state[6] == 0
                or self.grid_state[0] == cpu_char and self.grid_state[3] == cpu_char and self.grid_state[6] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[4] == cpu_char and self.grid_state[6] == 0
        ):
            winning_spaces.append(6)
        if (
                self.grid_state[6] == cpu_char and self.grid_state[8] == cpu_char and self.grid_state[7] == 0
                or self.grid_state[1] == cpu_char and self.grid_state[4] == cpu_char and self.grid_state[7] == 0
        ):
            winning_spaces.append(7)
        if (
                self.grid_state[6] == cpu_char and self.grid_state[7] == cpu_char and self.grid_state[8] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[5] == cpu_char and self.grid_state[8] == 0
                or self.grid_state[0] == cpu_char and self.grid_state[4] == cpu_char and self.grid_state[8] == 0
        ):
            winning_spaces.append(8)

        if len(winning_spaces) > 0:
            winning_choice = random.choice(winning_spaces)

        return winning_choice

    def find_one(self, cpu_char):
        """Allows the computer-controlled opponent to find a square which could lead to three in a row.

        Keyword arguments:
        cpu_char -- which character the computer-controlled opponent plays ('X' or 'O')
        """
        winning_spaces = []
        winning_choice = -1

        if (
                self.grid_state[1] == cpu_char and self.grid_state[2] == 0 and self.grid_state[0] == 0
                or self.grid_state[1] == 0 and self.grid_state[2] == cpu_char and self.grid_state[0] == 0
                or self.grid_state[3] == cpu_char and self.grid_state[6] == 0 and self.grid_state[0] == 0
                or self.grid_state[3] == 0 and self.grid_state[6] == cpu_char and self.grid_state[0] == 0
                or self.grid_state[4] == cpu_char and self.grid_state[8] == 0 and self.grid_state[0] == 0
                or self.grid_state[4] == 0 and self.grid_state[8] == cpu_char and self.grid_state[0] == 0
        ):
            winning_spaces.append(0)
        if (
                self.grid_state[0] == cpu_char and self.grid_state[2] == 0 and self.grid_state[1] == 0
                or self.grid_state[0] == 0 and self.grid_state[2] == cpu_char and self.grid_state[1] == 0
                or self.grid_state[4] == cpu_char and self.grid_state[7] == 0 and self.grid_state[1] == 0
                or self.grid_state[4] == 0 and self.grid_state[7] == cpu_char and self.grid_state[1] == 0
        ):
            winning_spaces.append(1)
        if (
                self.grid_state[0] == cpu_char and self.grid_state[1] == 0 and self.grid_state[2] == 0
                or self.grid_state[0] == 0 and self.grid_state[1] == cpu_char and self.grid_state[2] == 0
                or self.grid_state[5] == cpu_char and self.grid_state[8] == 0 and self.grid_state[2] == 0
                or self.grid_state[5] == 0 and self.grid_state[8] == cpu_char and self.grid_state[2] == 0
                or self.grid_state[4] == cpu_char and self.grid_state[6] == 0 and self.grid_state[2] == 0
                or self.grid_state[4] == 0 and self.grid_state[6] == cpu_char and self.grid_state[2] == 0
        ):
            winning_spaces.append(2)
        if (
                self.grid_state[4] == cpu_char and self.grid_state[5] == 0 and self.grid_state[3] == 0
                or self.grid_state[4] == 0 and self.grid_state[5] == cpu_char and self.grid_state[3] == 0
                or self.grid_state[0] == cpu_char and self.grid_state[6] == 0 and self.grid_state[3] == 0
                or self.grid_state[0] == 0 and self.grid_state[6] == cpu_char and self.grid_state[3] == 0
        ):
            winning_spaces.append(3)
        if (
                self.grid_state[0] == cpu_char and self.grid_state[8] == 0 and self.grid_state[4] == 0
                or self.grid_state[1] == cpu_char and self.grid_state[7] == 0 and self.grid_state[4] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[6] == 0 and self.grid_state[4] == 0
                or self.grid_state[3] == cpu_char and self.grid_state[5] == 0 and self.grid_state[4] == 0
                or self.grid_state[5] == cpu_char and self.grid_state[3] == 0 and self.grid_state[4] == 0
                or self.grid_state[6] == cpu_char and self.grid_state[2] == 0 and self.grid_state[4] == 0
                or self.grid_state[7] == cpu_char and self.grid_state[1] == 0 and self.grid_state[4] == 0
                or self.grid_state[8] == cpu_char and self.grid_state[0] == 0 and self.grid_state[4] == 0
        ):
            winning_spaces.append(4)
        if (
                self.grid_state[3] == cpu_char and self.grid_state[4] == 0 and self.grid_state[5] == 0
                or self.grid_state[3] == 0 and self.grid_state[4] == cpu_char and self.grid_state[5] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[8] == 0 and self.grid_state[5] == 0
                or self.grid_state[2] == 0 and self.grid_state[8] == cpu_char and self.grid_state[5] == 0
        ):
            winning_spaces.append(5)
        if (
                self.grid_state[7] == cpu_char and self.grid_state[8] == 0 and self.grid_state[6] == 0
                or self.grid_state[7] == 0 and self.grid_state[8] == cpu_char and self.grid_state[6] == 0
                or self.grid_state[0] == cpu_char and self.grid_state[3] == 0 and self.grid_state[6] == 0
                or self.grid_state[0] == 0 and self.grid_state[3] == cpu_char and self.grid_state[6] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[4] == 0 and self.grid_state[6] == 0
                or self.grid_state[2] == 0 and self.grid_state[4] == cpu_char and self.grid_state[6] == 0
        ):
            winning_spaces.append(6)
        if (
                self.grid_state[6] == cpu_char and self.grid_state[8] == 0 and self.grid_state[7] == 0
                or self.grid_state[6] == 0 and self.grid_state[8] == cpu_char and self.grid_state[7] == 0
                or self.grid_state[1] == cpu_char and self.grid_state[4] == 0 and self.grid_state[7] == 0
                or self.grid_state[1] == 0 and self.grid_state[4] == cpu_char and self.grid_state[7] == 0
        ):
            winning_spaces.append(7)
        if (
                self.grid_state[6] == cpu_char and self.grid_state[7] == 0 and self.grid_state[8] == 0
                or self.grid_state[6] == 0 and self.grid_state[7] == cpu_char and self.grid_state[8] == 0
                or self.grid_state[2] == cpu_char and self.grid_state[5] == 0 and self.grid_state[8] == 0
                or self.grid_state[2] == 0 and self.grid_state[5] == cpu_char and self.grid_state[8] == 0
                or self.grid_state[0] == cpu_char and self.grid_state[4] == 0 and self.grid_state[8] == 0
                or self.grid_state[0] == 0 and self.grid_state[4] == cpu_char and self.grid_state[8] == 0
        ):
            winning_spaces.append(8)

        if len(winning_spaces) > 0:
            winning_choice = random.choice(winning_spaces)

        return winning_choice
    
    def block_two(self, cpu_char):
        """Allows the computer-controlled opponent to find two squares with the character opposite the
        computer-controlled opponent's character.

        Keyword arguments:
        cpu_char -- which character the computer-controlled opponent plays ('X' or 'O')
        """
        if cpu_char == 1:
            block_char = 2
        else:
            block_char = 1

        return self.find_two(block_char)

    def human_take_turn(self, mouse_position):
        """Checks the human's mouse position on click to see if it's a valid choice or not.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if self.game_over == 0:
            if self.mouse_pos_0(mouse_position):
                self.set_grid(0)
            elif self.mouse_pos_1(mouse_position):
                self.set_grid(1)
            elif self.mouse_pos_2(mouse_position):
                self.set_grid(2)
            elif self.mouse_pos_3(mouse_position):
                self.set_grid(3)
            elif self.mouse_pos_4(mouse_position):
                self.set_grid(4)
            elif self.mouse_pos_5(mouse_position):
                self.set_grid(5)
            elif self.mouse_pos_6(mouse_position):
                self.set_grid(6)
            elif self.mouse_pos_7(mouse_position):
                self.set_grid(7)
            elif self.mouse_pos_8(mouse_position):
                self.set_grid(8)

        if self.mouse_pos_records(mouse_position):
            from RecordScreen import RecordScreen
            r = RecordScreen()
            r.init()
        elif self.mouse_pos_start(mouse_position):
            from StartScreen import StartScreen
            s = StartScreen()
            s.init()
            
    def set_grid(self, grid_position):
        """Sets the grid square to the correct character at the given position.

        Keyword arguments:
        grid_position -- the grid square to be changed
        """
        if self.grid_state[grid_position] == 0:
            if self.player_1_turn:
                if self.player_1_first:                   
                    self.grid_state[grid_position] = 1
                else:
                    self.grid_state[grid_position] = 2
            else:
                if self.player_1_first:
                    self.grid_state[grid_position] = 2
                else:
                    self.grid_state[grid_position] = 1
            self.player_1_turn = not self.player_1_turn
            if self.cpu_opponent:
                self.cpu_turn = True

    def draw_x(self, pos_x, pos_y):
        """Draws an 'X' in the correct place.

        Keyword arguments:
        pos_x -- the top left X position
        pos_y -- the top left Y position
        """
        pygame.draw.line(self.display, self.black, (pos_x, pos_y), (pos_x + 90, pos_y + 90), 3)
        pygame.draw.line(self.display, self.black, (pos_x, pos_y + 90), (pos_x + 90, pos_y), 3)

    def draw_o(self, pos_x, pos_y):
        """Draws an 'O' in the correct place.

        Keyword arguments:
        pos_x -- the top left X position
        pos_y -- the top left Y position
        """
        pygame.draw.circle(self.display, self.black, (pos_x, pos_y), 45, 1)

    def draw_win_line(self):
        """Draws a red line through the three winning characters."""
        if self.grid_state[0] == self.grid_state[1] == self.grid_state[2] and self.grid_state[0] != 0:
            pygame.draw.line(self.display, self.red, (205, 50), (495, 50), 4)
        elif self.grid_state[3] == self.grid_state[4] == self.grid_state[5] and self.grid_state[3] != 0:
            pygame.draw.line(self.display, self.red, (205, 150), (495, 150), 4)
        elif self.grid_state[6] == self.grid_state[7] == self.grid_state[8] and self.grid_state[6] != 0:
            pygame.draw.line(self.display, self.red, (205, 250), (495, 250), 4)
        elif self.grid_state[0] == self.grid_state[3] == self.grid_state[6] and self.grid_state[0] != 0:
            pygame.draw.line(self.display, self.red, (250, 5), (250, 295), 4)
        elif self.grid_state[1] == self.grid_state[4] == self.grid_state[7] and self.grid_state[1] != 0:
            pygame.draw.line(self.display, self.red, (350, 5), (350, 295), 4)
        elif self.grid_state[2] == self.grid_state[5] == self.grid_state[8] and self.grid_state[2] != 0:
            pygame.draw.line(self.display, self.red, (450, 5), (450, 295), 4)
        elif self.grid_state[0] == self.grid_state[4] == self.grid_state[8] and self.grid_state[0] != 0:
            pygame.draw.line(self.display, self.red, (205, 5), (495, 295), 4)
        elif self.grid_state[2] == self.grid_state[4] == self.grid_state[6] and self.grid_state[2] != 0:
            pygame.draw.line(self.display, self.red, (495, 5), (205, 295), 4)

    def check_win(self):
        """Checks to see if a win-state has been reached. Returns 1 if 'X' wins, 2 if 'O' wins, 3 if it's a draw and 0
        if a win-state has not been reached."""
        if (
                self.grid_state[0] == 1 and self.grid_state[1] == 1 and self.grid_state[2] == 1
                or self.grid_state[3] == 1 and self.grid_state[4] == 1 and self.grid_state[5] == 1
                or self.grid_state[6] == 1 and self.grid_state[7] == 1 and self.grid_state[8] == 1
                or self.grid_state[0] == 1 and self.grid_state[3] == 1 and self.grid_state[6] == 1
                or self.grid_state[1] == 1 and self.grid_state[4] == 1 and self.grid_state[7] == 1
                or self.grid_state[2] == 1 and self.grid_state[5] == 1 and self.grid_state[8] == 1
                or self.grid_state[0] == 1 and self.grid_state[4] == 1 and self.grid_state[8] == 1
                or self.grid_state[2] == 1 and self.grid_state[4] == 1 and self.grid_state[6] == 1
        ):
            return 1
        elif (
                self.grid_state[0] == 2 and self.grid_state[1] == 2 and self.grid_state[2] == 2
                or self.grid_state[3] == 2 and self.grid_state[4] == 2 and self.grid_state[5] == 2
                or self.grid_state[6] == 2 and self.grid_state[7] == 2 and self.grid_state[8] == 2
                or self.grid_state[0] == 2 and self.grid_state[3] == 2 and self.grid_state[6] == 2
                or self.grid_state[1] == 2 and self.grid_state[4] == 2 and self.grid_state[7] == 2
                or self.grid_state[2] == 2 and self.grid_state[5] == 2 and self.grid_state[8] == 2
                or self.grid_state[0] == 2 and self.grid_state[4] == 2 and self.grid_state[8] == 2
                or self.grid_state[2] == 2 and self.grid_state[4] == 2 and self.grid_state[6] == 2
        ):
            return 2
        elif (
                self.grid_state[0] != 0 and self.grid_state[1] != 0 and self.grid_state[2] != 0
                and self.grid_state[3] != 0 and self.grid_state[4] != 0 and self.grid_state[5] != 0
                and self.grid_state[6] != 0 and self.grid_state[7] != 0 and self.grid_state[8] != 0
        ):
            return 3
        else:
            return 0

    def save_game(self):
        """Stores the results of the game in the database table."""
        if not self.game_saved:
            winner = ""
            character = ""
            turns = 0
            date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            difficulty = ""

            if self.game_over == 1:
                if self.cpu_opponent:
                    if self.cpu_x:
                        winner = "Computer"
                    else:
                        winner = "Human"
                else:
                    if self.player_1_first:
                        winner = "Player 1"
                    else:
                        winner = "Player 2"
                character = "X"
            elif self.game_over == 2:
                if self.cpu_opponent:
                    if self.cpu_x:
                        winner = "Human"
                    else:
                        winner = "Computer"
                else:
                    if self.player_1_first:
                        winner = "Player 2"
                    else:
                        winner = "Player 1"
                character = "O"
            elif self.game_over == 3:
                winner = "Draw"
                character = "NA"

            if self.cpu_opponent:
                if self.cpu_difficulty == 0:
                    difficulty = "Easy"
                elif self.cpu_difficulty == 1:
                    difficulty = "Medium"
                elif self.cpu_difficulty == 2:
                    difficulty = "Hard"

            for space in self.grid_state:
                if space > 0:
                    turns = turns + 1

            self.conn.execute(f'INSERT INTO records VALUES ("{date}", "{winner}", "{character}", "{turns}", "{difficulty}")')
            self.conn.commit()

            self.game_saved = True

    def draw_background(self):
        """Draws the grid for the game."""
        self.display.fill(self.white)

        pygame.draw.line(self.display, self.black, (200, 0), (200, 300), 1)
        pygame.draw.line(self.display, self.black, (300, 0), (300, 300), 1)
        pygame.draw.line(self.display, self.black, (400, 0), (400, 300), 1)
        pygame.draw.line(self.display, self.black, (200, 100), (500, 100), 1)
        pygame.draw.line(self.display, self.black, (200, 200), (500, 200), 1)

    def mouse_pos_start(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Start Screen'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 38 < mouse_position[0] < 162 and 187 < mouse_position[1] < 210:
            return True
        else:
            return False

    def mouse_pos_records(self, mouse_position):
        """Returns whether or not the mouse cursor is over 'Records'.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 59 < mouse_position[0] < 141 and 239 < mouse_position[1] < 258:
            return True
        else:
            return False

    def mouse_pos_0(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 0.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 200 < mouse_position[0] < 300 and 0 < mouse_position[1] < 100:
            return True
        else:
            return False

    def mouse_pos_1(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 1.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 300 < mouse_position[0] < 400 and 0 < mouse_position[1] < 100:
            return True
        else:
            return False

    def mouse_pos_2(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 2.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 400 < mouse_position[0] < 500 and 0 < mouse_position[1] < 100:
            return True
        else:
            return False

    def mouse_pos_3(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 3.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 200 < mouse_position[0] < 300 and 100 < mouse_position[1] < 200:
            return True
        else:
            return False

    def mouse_pos_4(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 4.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 300 < mouse_position[0] < 400 and 100 < mouse_position[1] < 200:
            return True
        else:
            return False

    def mouse_pos_5(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 5.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 400 < mouse_position[0] < 500 and 100 < mouse_position[1] < 200:
            return True
        else:
            return False

    def mouse_pos_6(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 6.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 200 < mouse_position[0] < 300 and 200 < mouse_position[1] < 300:
            return True
        else:
            return False

    def mouse_pos_7(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 7.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 300 < mouse_position[0] < 400 and 200 < mouse_position[1] < 300:
            return True
        else:
            return False

    def mouse_pos_8(self, mouse_position):
        """Returns whether or not the mouse cursor is over grid square 8.

        Keyword arguments:
        mouse_position -- Tuple containing the X and Y positions of the mouse cursor
        """
        if 400 < mouse_position[0] < 500 and 200 < mouse_position[1] < 300:
            return True
        else:
            return False

    def run_screen(self):
        """Runs the Game Screen.

        Checks for any events (mouse events, etc.) and does appropriate action.
        Displays any text or other images on the display.
        """
        self.create_table()
        self.draw_background()
        if self.cpu_opponent:
            if self.cpu_turn:
                self.display_message('Computer Turn', 100, 50)
            else:
                self.display_message('Human Turn', 100, 50)
            self.display_message('Start Screen', 100, 200, 20)
            self.display_message('Records', 100, 250, 20)
        pygame.display.flip()

        while 1:
            self.draw_background()
            if self.cpu_turn and self.cpu_opponent and self.game_over == 0:
                self.cpu_take_turn()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.conn.close()
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        mouse_position = pygame.mouse.get_pos()
                        if (
                                self.mouse_pos_0(mouse_position) and self.grid_state[0] == 0
                                or self.mouse_pos_1(mouse_position) and self.grid_state[1] == 0
                                or self.mouse_pos_2(mouse_position) and self.grid_state[2] == 0
                                or self.mouse_pos_3(mouse_position) and self.grid_state[3] == 0
                                or self.mouse_pos_4(mouse_position) and self.grid_state[4] == 0
                                or self.mouse_pos_5(mouse_position) and self.grid_state[5] == 0
                                or self.mouse_pos_6(mouse_position) and self.grid_state[6] == 0
                                or self.mouse_pos_7(mouse_position) and self.grid_state[7] == 0
                                or self.mouse_pos_8(mouse_position) and self.grid_state[8] == 0
                                or self.mouse_pos_start(mouse_position)
                                or self.mouse_pos_records(mouse_position)
                        ):
                            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                        else:
                            pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self.human_take_turn(mouse_position)

            if self.grid_state[0] == 1:
                self.draw_x(205, 5)
            elif self.grid_state[0] == 2:
                self.draw_o(250, 50)

            if self.grid_state[1] == 1:
                self.draw_x(305, 5)
            elif self.grid_state[1] == 2:
                self.draw_o(350, 50)

            if self.grid_state[2] == 1:
                self.draw_x(405, 5)
            elif self.grid_state[2] == 2:
                self.draw_o(450, 50)

            if self.grid_state[3] == 1:
                self.draw_x(205, 105)
            elif self.grid_state[3] == 2:
                self.draw_o(250, 150)

            if self.grid_state[4] == 1:
                self.draw_x(305, 105)
            elif self.grid_state[4] == 2:
                self.draw_o(350, 150)

            if self.grid_state[5] == 1:
                self.draw_x(405, 105)
            elif self.grid_state[5] == 2:
                self.draw_o(450, 150)

            if self.grid_state[6] == 1:
                self.draw_x(205, 205)
            elif self.grid_state[6] == 2:
                self.draw_o(250, 250)

            if self.grid_state[7] == 1:
                self.draw_x(305, 205)
            elif self.grid_state[7] == 2:
                self.draw_o(350, 250)

            if self.grid_state[8] == 1:
                self.draw_x(405, 205)
            elif self.grid_state[8] == 2:
                self.draw_o(450, 250)

            if self.game_over == 0:
                if self.cpu_opponent:
                    if self.cpu_turn:
                        self.display_message('Computer Turn', 100, 50)
                    else:
                        self.display_message('Human Turn', 100, 50)
                else:
                    if self.player_1_turn:
                        self.display_message('Player 1 Turn', 100, 50)
                    else:
                        self.display_message('Player 2 Turn', 100, 50)

            self.game_over = self.check_win()
            if self.game_over != 0:
                if self.game_over == 1:
                    if self.cpu_opponent:
                        if self.cpu_x:
                            self.display_message('Computer Wins!', 100, 50, 14, self.red)
                        else:
                            self.display_message('Human Wins!', 100, 50, 14, self.red)
                    else:
                        if self.player_1_first:
                            self.display_message('Player 1 Wins!', 100, 50, 14, self.red)
                        else:
                            self.display_message('Player 2 Wins!', 100, 50, 14, self.red)
                elif self.game_over == 2:
                    if self.cpu_opponent:
                        if self.cpu_x:
                            self.display_message('Human Wins!', 100, 50, 14, self.red)
                        else:
                            self.display_message('Computer Wins!', 100, 50, 14, self.red)
                    else:
                        if self.player_1_first:
                            self.display_message('Player 2 Wins!', 100, 50, 14, self.red)
                        else:
                            self.display_message('Player 1 Wins!', 100, 50, 14, self.red)
                elif self.game_over == 3:
                    self.display_message('Draw', 100, 50)

                self.draw_win_line()
                self.save_game()

            self.display_message('Start Screen', 100, 200, 20)
            self.display_message('Records', 100, 250, 20)

            pygame.display.flip()
