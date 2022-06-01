import pygame

class InputBox():
    
    def __init__(self, x, y):
        
        self.font = pygame.font.Font("assets/font.ttf", 20)
        self.rect = pygame.Rect(x, y, 160, 30)
        self.color_inactive = pygame.Color('#bbe6f4')
        self.color_active = pygame.Color('white')
        self.color = self.color_inactive
        self.text = ''

        self.active = False
        
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
    
    def draw(self, screen):
        text_image = self.font.render(self.text, True, "Black")
        text_rect = text_image.get_rect()
        self.rect.w = max(200, text_rect.w+10)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text_image, (self.rect.x+5, self.rect.y+5))

    def returntext(self):
        return self.text