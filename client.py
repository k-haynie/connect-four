import pygame
import pyfxr
from pygame.locals import *
from gameClasses import *

class connectFour():
    def __init__(self):
        self.screen = pygame.display.set_mode(      # set the window size to 1280 x 720
            (1280, 720))
        pygame.display.set_caption("Connect Four")
        pygame.display.set_icon(pygame.image.load("red_token.png"))
        
        self.font = pygame.font.Font('Sansation-Bold.ttf', 32)# set the font type and size
        self.title = pygame.font.Font('Sansation-Bold.ttf', 48)
        self.clock = pygame.time.Clock()            # set a variable for limiting FPS
        self.center = pygame.Vector2(               # establish the center (x,y) coords of the screen
            self.screen.get_width()/2, self.screen.get_height()/2)
        self.bkgColor = "gray"                      # sets the background color
        self.screen.fill(self.bkgColor)                    # paint the game screen gray
        self.COLORS = COLORS()

        self.active = True                          # this controls the otherwise-infine rendering loop
        self.game_running = False                   # this controls whether the menu or the board is drawn
        self.new_game = False                       # this controls whether a new game is started after the current game ends
        self.player_turn = 1                        # this controls the current player (1 or 2)
        self.board = [[0 for i in range(6)] for j in range(7)]    # this creates a 6 x 7 board to use as a reference for win-checking

        self.tokens = pygame.sprite.Group()         # this tracks the black game board circles
        self.positions = pygame.sprite.Group()      # this tracks the clickable "position" circles
        self.buttons = pygame.sprite.Group()        # this tracks any rendered buttons
        self.text = pygame.sprite.Group()           # this tracks any rendered text rectangles
        self.render_menu()                          # this draws the menu screen at the end of the new connectFour initialization

    def play_drop_sound(self):
        tone = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=1.0, pitch='A4'))
        tone.play()

    def play_begin_sound(self):
        do = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.2, pitch='C4'))
        mi = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.2, pitch='E4'))
        sol = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.2, pitch='G4'))
        do2 = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.2, pitch='C5'))

        do.play()
        pygame.time.wait(200)  # Add a delay between notes (in milliseconds)
        mi.play()
        pygame.time.wait(200)
        sol.play()
        pygame.time.wait(200)
        do2.play()

    def play_win_sound(self):
        do = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.5, pitch='C4'))
        mi = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.5, pitch='E4'))
        sol = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.5, pitch='G4'))
        do2 = pygame.mixer.Sound(buffer=pyfxr.pluck(duration=0.5, pitch='C5'))
    
        pygame.time.wait(500)
        do2.play()
        pygame.time.wait(200)
        sol.play()
        pygame.time.wait(200)  # Add a delay between notes (in milliseconds)
        mi.play()
        pygame.time.wait(200)
        do.play()

    # returns the color associated with the current player
    def player_color(self) -> str:
        return self.COLORS.red if self.player_turn == 1 else self.COLORS.blue

    # paint the screen gray, draw the black tokens and "drop" placeholders
    def render_tokens(self):
        self.draw_board()

        # I used manual coordinates because mental math is fun
        for i in [400, 480, 560, 640, 720, 800, 880]:
            for j in [140, 240, 320, 400, 480, 560, 640]:
                if j == 140:
                    # add the placeholders at the top and give them optional column-id values
                    column_val = int((i-400)/80)
                    self.positions.add(Token(self.screen, "darkgrey", [i, j], 30, column_val))     
                else:
                    
                    self.tokens.add(Token(self.screen, "gray", [i, j], 30, self.bkgColor))     

    # re-renders necessary background props
    def draw_board(self):
        self.screen.fill(self.bkgColor)
        pygame.draw.rect(self.screen, (222, 151, 11), pygame.Rect(335, 185, 610, 510), border_radius=20)
        pygame.draw.rect(self.screen, self.COLORS.yellow, pygame.Rect(340, 190, 600, 500), border_radius=20)

        # drawk token outlines
        for i in [400, 480, 560, 640, 720, 800, 880]:
            for j in [240, 320, 400, 480, 560, 640]:
                    Token(self.screen, "black", [i, j], 33, self.bkgColor)

    # check the game board for 4 in a row and return a boolean value
    def check_for_winner(self) -> bool:
        # make a list of strings for each column sequence
        column_strs = ["".join(str(col) for col in row) for row in self.board]

        # make a list of strings for each row sequence
        row_strs = ["".join(row[j] for row in column_strs) for j in range(len(column_strs[0]))]

        # make a list of strings for each diagonal sequence
        diagonal_strs = self.get_diagonals()

        # check each of the sequences for a substring of either 
        # '1111' or '2222' given the current player
        for seq in column_strs + row_strs + diagonal_strs:
            if (str(self.player_turn)*4) in seq:
                return True
            
        full_board = True
        for seq in column_strs + row_strs + diagonal_strs:
            if "0" in seq:
                full_board = False
                break

        if full_board:
            self.player_turn = None
            return True
        
        return False

    # return a list of diagonals as strings
    def get_diagonals(self):
        diagonals = []

        # left/up to right/down diagonals
        for i in [[3, 0], [2, 0], [1, 0], [0, 0], [0, 1], [0, 2]]:
            diagonals.append(self.get_diagonal_start_with(i[0], i[1], ""))

        # right/up to left/down diagonals
        for i in [[0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5]]:
            diagonals.append(self.get_diagonal_start_with(i[0], i[1], "", True))

        return diagonals

    # recursively get the strings of diagonal values
    def get_diagonal_start_with(self, i, j, string, backwards=False):
        # this algorithm takes a starting coordinate and wither works down and to the right (not backwards)
        # or down and to the left (backwards) until it hits the end of the board. It returns a string 
        # representing the sequence of values for that diagonal strip.
    
        if not backwards:
            if i < 6 and j < 5:
                return string + self.get_diagonal_start_with(i + 1, j + 1, str(self.board[i][j]))
        else:
            if i < 6 and j > 0:
                return string + self.get_diagonal_start_with(i + 1, j - 1, str(self.board[i][j]), True)
            
        return string + str(self.board[i][j])

    # renders the game title and play button
    def render_menu(self):
        text = self.title.render("Connect Four", True, "black")

        # change the position of the text's rectangle to be horizontally centered and 200px above dead center
        x, y, w, h = text.get_rect()
        textRect = (self.center.x - (w / 2), self.center.y - 200, w, h)

        # draw the button and add to the list of sprites to track
        self.screen.blit(text, textRect) 
        self.buttons.add(Button(self.screen, "white", COLORS().btnBlue, "Begin", self.title, self.center.x, self.center.y))

    # updates the game screen with the current player
    def announce_player(self, winner = False):
        # creates a text object and moves to be 300px above dead center
        msg = f"Player {self.player_turn}'s turn" if not winner else (f"Player {self.player_turn} wins!" if self.player_turn != None else "The game is a draw!")
        text = self.font.render(msg, True, self.player_color(), self.bkgColor)
        x, y, w, h = text.get_rect()
        textRect = (self.center.x - (w / 2), self.center.y - 320, w, h)

        pygame.draw.rect(self.screen, self.bkgColor, pygame.Rect(textRect[0] - 10, textRect[1] - 10, textRect[2] + 20, textRect[3] + 20))
        self.screen.blit(text, textRect) # draws the text in the given textRect rectangle

    # tries to drop a token, returns bool for success
    def drop(self, col) -> bool:
        tokensList = self.tokens.sprites()
        index = col * 6 + 5
        success = False

        # iteratively test each token until the top 
        # of the column is reached or an empty slot is found
        while index >= col*6 and not success:
            token = tokensList[index]
            if token.color == token.real_color:
                token.newColor(self.player_color())

                self.board[index // 6][index % 6] = self.player_turn
                success = True
            else:
                index -= 1

        return success

    # declares a winner
    def handle_win(self):
        self.game_running = False
        self.announce_player(True)
        self.positions.empty()
        self.buttons.add(Button(self.screen, "white", self.COLORS.btnBlue, "Play Again?", self.font, self.center.x, self.center.y))
        self.play_win_sound()

    # manages the main game rendering loop
    def game_loop(self):
        while self.active:
            for event in pygame.event.get():

                # detects a window close
                if event.type == pygame.QUIT:
                    self.active = False

                elif event.type == MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()       # get the mouse's (x,y) coords

                    # if there is a button and the mouse clicked it, start the game
                    if self.buttons and self.buttons.sprites()[0].get_rect().collidepoint(mousePos):
                        if self.buttons.sprites()[0].get_msg() == "Begin":
                            self.buttons.empty()                # removes the button from the sprite list
                            self.render_tokens()                # draws the game board
                            self.announce_player()              # draws the current player
                            self.game_running = True            # sets the game_running variable
                            self.play_begin_sound()

                        elif self.buttons.sprites()[0].get_msg() == "Play Again?":
                            self.active = False
                            self.new_game = True
                    
                    # loops over all the tokens and checks for mouse collisions
                    for token in self.positions:
                        if self.game_running and token.get_rect().collidepoint(mousePos): 
                            
                            column = token.get_id()             # gets the column number of the clicked position
                            if self.drop(column):               # tries to drop a player token in the column
                                self.play_drop_sound()

                                if self.check_for_winner():
                                    self.handle_win()           
                                else:
                                    self.player_turn = 1 if self.player_turn == 2 else 2
                                    self.announce_player()
                                
            # trigger the token rendering if the mouse is over a playable column    
            if self.game_running:
                for token in self.positions:
                    token.hover_toggle(self.player_color())
                    
            # trigger the recoloring-on-hover for any screen buttons
            for button in self.buttons:
                button.hover_toggle()

            # redraw any graphics updates
            pygame.display.flip()

            # limit the FPS to 60
            self.clock.tick(60)

        return self.new_game

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.init()

    startGame = True
    while startGame:
        startGame = connectFour().game_loop()

    pygame.quit()