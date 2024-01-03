import pygame

class COLORS:
    def __init__(self):
        self.yellow = (222, 194, 11)
        self.blue = (17, 117, 168)
        self.red = (187, 0, 0)
        self.btnBlue = (15, 82, 186)

class Token(pygame.sprite.Sprite):
    def __init__(self, screen, color, x, y, id = None):
        pygame.sprite.Sprite.__init__(self)     # initialize the parent Sprite class
        self.x, self.y = x, y           # sets the x and y coordinates
        self.screen = screen            # sets the screen to draw on
        self.color = color              # sets the background color of the tokens
        self.real_color = color         # sets the intended color of the tokens, if they toggle
        self.id = id                    # sets a column id, if provided

        self.draw_token()               # finally, draw the token

    # returns the bounding rectangle
    def get_rect(self):
        return self.rect
    
    # returns the column id
    def get_id(self):
        return self.id
    
    # changes the token color
    def newColor(self, color):
        self.color = color
        self.draw_token()

    # draws the token on the screen 
    def draw_token(self):
        self.rect = pygame.draw.circle(self.screen, self.color, self.x, self.y)
        if self.color in [COLORS().red, COLORS().blue]:
            pygame.draw.circle(self.screen, "darkred" if self.color == COLORS().red else "darkslategray", self.x, 25, width=3)

        pygame.display.update()

    # toggle the token recoloring, if applicable
    def hover_toggle(self, color):
        if self.get_rect().collidepoint(pygame.mouse.get_pos()) and self.color != color:
            self.newColor(color)
        elif not self.get_rect().collidepoint(pygame.mouse.get_pos()) and self.color != self.real_color:
            self.newColor(self.real_color)

class Button(pygame.sprite.Sprite):
    def __init__(self, screen, fontColor, bkgColor, message, font, x, y, rad=20, hover=True):
        pygame.sprite.Sprite.__init__(self)     # initialize the parent Sprite class
        self.x, self.y = x, y           # establish x and y coordinates
        self.rad = rad                  # set corner radius
        self.hover = hover              # determines whether a recolor is caused on mouse hover
        self.message = message          # sets the button text
        self.screen = screen            # sets the screen to draw on
        self.font = font                # sets the font class
        self.fontColor = fontColor      # sets the font color
        self.bkgColor = bkgColor        # sets the reference background color
        self.buttonColor = bkgColor     # conrols the actual rendered button background color
        self.rect = None                # makes a class-wide accessible rect property
        
        self.draw_button()              # finally, draw the button to the screen

    # return the rectangle coordinates of the button
    def get_rect(self):                 
        return self.rect
    
    # return the button's text
    def get_msg(self):
        return self.message

    # toggle the button's background color if pertinent
    def hover_toggle(self, color="darkblue"):
        if self.hover and self.get_rect().collidepoint(pygame.mouse.get_pos()) and self.buttonColor == self.bkgColor:
            self.buttonColor = color
            self.draw_button()
        elif self.hover and not self.get_rect().collidepoint(pygame.mouse.get_pos()) and self.buttonColor == color:
            self.buttonColor = self.bkgColor
            self.draw_button()

    # render the text, the rect, update the game screen 
    def draw_button(self):
        text = self.font.render(self.message, True, self.fontColor)
        x, y, w, h = text.get_rect()
        textRect = (self.x - (w/2), self.y - (h/2), w, h)

        pygame.draw.rect(self.screen, "darkslategray", pygame.Rect(textRect[0] - 35, textRect[1] - 35, w + 70, h + 70), border_radius=self.rad)
        self.rect = pygame.draw.rect(self.screen, self.buttonColor, pygame.Rect(textRect[0] - 30, textRect[1] - 30, w + 60, h + 60), border_radius=self.rad)
        self.screen.blit(text, textRect)  
        pygame.display.update()