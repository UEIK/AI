from program import *

class Button():
    def __init__(self, x_pos, y_pos, text_input, w=200, h=75):
        self.image = pygame.transform.scale(pygame.image.load("img/button.png"), (w, h))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.selected = False
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = FONT.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        DISPLAYSURF.blit(self.image, self.rect)
        DISPLAYSURF.blit(self.text, self.text_rect)

    def checkForInput(self, position, event):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound("sound/click.wav").play()
                self.text = FONT.render(self.text_input, True, PINK)
                return True
        else:
            if self.selected:
                self.text = FONT.render(self.text_input, True, PINK)
            else:
                self.text = FONT.render(self.text_input, True, "white")
            self.update()
            return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = FONT.render(self.text_input, True, "pink")
        else:
            self.text = FONT.render(self.text_input, True, "white")

    def set_selected(self, selected):
        self.selected = selected