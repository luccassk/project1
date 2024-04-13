import sys

import pygame
from pygame import mixer
from maps import level_map
mixer.init()

#მუსიკების შემოტანა
# mixer.music.load("images/jungles.ogg")
# mixer.music.play(-1)


pygame.init()
clock = pygame.time.Clock()

width = 1000
height = 700

size = (50, 50)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MazeGame")

cyborg_image = pygame.image.load("images/cyborg.png").convert_alpha()
cyborg_image = pygame.transform.scale(cyborg_image, size)
pygame.display.set_icon(cyborg_image)

background = pygame.image.load("images/background3.jpg").convert_alpha()
background = pygame.transform.scale(background, (width, height))

text = 'You Loose'
color = (255, 40, 40)

class BackgroundClass:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)


background_group = []

for y, line in enumerate(level_map):
    for x, symbol in enumerate(line):
        if symbol == " ":
            pass
        else:
            new_block = BackgroundClass(x * 50, y * 50)
            background_group.append(new_block)







class BaseClass:
    def __init__(self, image, x, y):
        self.right_image = image
        self.image = image
        self.rect = image.get_rect(centerx=x, centery=y)
        self.dx = 0
        self.dy = 0

    def draw(self):
        screen.blit(self.image, self.rect)

        if self.dx > 0:
            self.image = self.right_image
        if self.dx < 0:
            self.image = pygame.transform.flip(self.right_image, True, False)

    def movement(self):
        pass

    def update(self):
        self.movement()
        self.draw()


class Player(BaseClass):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def movement(self):
        global run, text, color
        self.dx = 0
        self.dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.dy == 0:
            self.dx = 5
        if key[pygame.K_LEFT] and self.dy == 0:
            self.dx = -5
        if key[pygame.K_UP] and self.dx == 0:
            self.dy = -5
        if key[pygame.K_DOWN] and self.dx == 0:
            self.dy = 5

        self.rect.x += self.dx
        self.rect.y += self.dy

        # ეკრანს არ გაცდეს
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

        #თამაშის წაგება
        if self.rect.colliderect(cyborg.rect):
            run = False

        # თამაშის მოგება
        if self.rect.colliderect(treasure_rect):
            run = False
            text = "You Win!"
            color = (200, 200, 40)

        for block in background_group:
            if block.rect.colliderect(self.rect):
                if self.dx > 0 and self.rect.right > block.rect.left:
                    self.rect.right = block.rect.left

                if self.dx < 0 and self.rect.left < block.rect.right:
                    self.rect.left = block.rect.right

                if self.dy > 0 and self.rect.bottom > block.rect.top:
                    self.rect.bottom = block.rect.top

                if self.dy < 0 and self.rect.top < block.rect.bottom:
                    self.rect.top = block.rect.bottom






class Enemy(BaseClass):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.dx = 5

    def movement(self):

        if self.rect.left <= 700 and self.dx < 0:
            self.dx *= -1
        elif self.rect.right >= width and self.dx > 0:
            self.dx *= -1

        self.rect.x += self.dx



player_image = pygame.image.load("images/hero.png").convert_alpha()
player_image = pygame.transform.scale(player_image, size)
player = Player(player_image, 300, 300)
cyborg = Enemy(cyborg_image, 700, 550)


treasure = pygame.image.load("images/treasure.png").convert_alpha()
treasure = pygame.transform.scale(treasure, size)
treasure_rect = treasure.get_rect(centerx=850, centery=650)


font = pygame.font.Font(None, 120)

def game_over(text, color):
    rendered_text = font.render(text, True, color)
    rect = rendered_text.get_rect(centerx=width/2, centery=height/2)
    screen.blit(rendered_text, rect)


run = True
while run:
    clock.tick(60)
    screen.blit(background, (0, 0))
    screen.blit(treasure, treasure_rect)

    for block in background_group:
        block.draw()

    player.update()
    cyborg.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


game_over(text, color)
pygame.display.update()
pygame.time.wait(3000)

pygame.quit()
sys.exit()