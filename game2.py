import sys
import pygame
from random import randint
from pygame import mixer
#ფაიგეიმის ინიციაცია
pygame.init()
mixer.init()
#ეკრანის ზომები
width = 700
height = 700

mixer.music.load("images/spacesound.mp3")
mixer.music.play(-1)

shooting_sound = mixer.Sound("images/blaster-2-81267.mp3")
game_over_sound = mixer.Sound("images/gameover.mp3")


background_img = pygame.image.load("images/background2.png")
background_img = pygame.transform.scale(background_img, (700, 700))
player_img = pygame.image.load("images/spaceship.png")
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.image.load("images/alien.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
enemy_img1 = pygame.image.load("images/alien.png")
enemy_img1 = pygame.transform.scale(enemy_img1, (50, 50))



#ეკრანის შექმნა
screen = pygame.display.set_mode((width, height))
#ეკრანის წარწერის ცვლილება
pygame.display.set_caption("Shooter Game")
pygame.display.set_icon(player_img)
clock = pygame.time.Clock()

bullet_group = pygame.sprite.Group()

score = 0
missed = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # მოთამაშის კვადრატის შექმნა
        self.rect = pygame.Rect(x, y, 5, 10)
        #მოთამაშის კვადრატის ლოკაციის მინიჭება
        self.rect.center = [x, y]
        self.speed = -5

    def draw(self):
        #მოთამაშის კვადრატის დახატვა ეკრანზე
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def movement(self):
        self.rect.y += self.speed

    def update(self):
        global score
        self.draw()
        self.movement()

        if self.rect.bottom < 0:
            self.kill()

        for sprite in enemy_group:
            if self.rect.colliderect(sprite.rect):
                score += 1
                self.kill()
                sprite.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img1, img2, speed):
        super().__init__()
        self.image = img1
        self.img1 = img1
        self.img2 = img2
        self.size = 50
        self.x = randint(self.size+25, width-self.size-25)
        self.y = randint(-500, -100)

        # მოთამაშის კვადრატის შექმნა
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        #მოთამაშის კვადრატის ლოკაციის მინიჭება
        self.rect.center = [self.x, self.y]
        self.speed = speed
        #ანიმაციისთვის მთვლელის შექმნა
        self.counter = 0

    def draw(self):
        #მოთამაშის კვადრატის დახატვა ეკრანზე
        # pygame.draw.rect(screen, (255, 255, 40), self.rect)
        screen.blit(self.image, self.rect)

    def movement(self):
        self.rect.y += self.speed

    def update(self):
        global missed
        self.draw()
        self.movement()

        #ყოველ ნახევარ წამში სურათის შეცვლა
        self.counter += 1
        if self.counter == 80:
            self.counter = 0

            if self.image == self.img1:
                self.image = self.img2
            elif self.image == self.img2:
                self.image = self.img1


        if self.rect.top > height:
            missed += 1
            self.kill()



#მოთამაშის კლასი
class Player:
    def __init__(self, img):
        self.size = 50
        self.image = img
        # მოთამაშის კვადრატის შექმნა
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        #მოთამაშის კვადრატის ლოკაციის მინიჭება
        self.rect.center = [width/2, height-100]
        self.speed = 1
        #გასროლის წამმზომის შექმნა
        self.counter = 0
        #გასროლის უფლების ცვლადი
        self.shoot = True

    def draw(self):
        #მოთამაშის კვადრატის დახატვა ეკრანზე
        # pygame.draw.rect(screen, (255, 255, 255), self.rect)
        screen.blit(self.image, self.rect)

    def movement(self):
        dx = 0
        #კლავიშების კონტროლი
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            dx = self.speed

        if key[pygame.K_LEFT]:
            dx = -self.speed
        #გასროლის კონტროლი
        if key[pygame.K_SPACE] and self.shoot:
            self.shoot = False
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            shooting_sound.play()
            bullet_group.add(bullet)

        #ეკრანის შემოსაზღვრის კოდი
        if self.rect.right > width-50:
            dx = 0
            self.rect.right = width-50

        if self.rect.left < 50:
            dx = 50
            self.rect.left = 0
        #მოძრაობა ჰორიზონტალზე
        self.rect.x += dx

    def update(self):
        self.draw()
        self.movement()

        #სროლის წამზომის კონტროლი
        if self.shoot == False:
            self.counter += 1

        if self.counter >= 60:
            self.counter = 0
            self.shoot = True


#მოთამაშის კლასისგან ობიექტის შექმნა
player1 = Player(player_img)

#მოწინააღმდეგის შესაქმნელი მთვლელი
timer = 160 * 2

enemy_group = pygame.sprite.Group()

font_score = pygame.font.Font(None, 30)

def write_info():
    render_text1 = font_score.render(f"Score: {score}", True, (255, 255, 255))
    render_text2 = font_score.render(f"Missed: {missed}", True, (255, 255, 255))

    screen.blit(render_text1, (10, 10))
    screen.blit(render_text2, (10, 30))


font_over = pygame.font.Font(None, 90)

def game_over():
    render_text = font_over.render("Game Over", True, (255, 255, 255))
    rect = render_text.get_rect()
    rect.center = [width/2, height/2]
    screen.blit(render_text, rect)


start_speed = 1
run = True
while run:
    clock.tick(160)
    #ეკრანში ფერის ჩასხმა
    screen.fill((128, 0, 128))
    screen.blit(background_img, (0, 0))




    bullet_group.update()
    enemy_group.update()
    #მოთამაშის ობიექტის კვადრატის დახატვა ეკრანზე
    player1.update()
    #თამაშის გათიშვა თუკი იქსიკს დავაწვებით ეკრანის ზედა მარჯვენა კუთხეში
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #მოწინააღმდეგის შექმნა
    if timer > 0:
        timer -= 1
    else:
        start_speed += 0.01
        enemy = Enemy(enemy_img, enemy_img1, start_speed)
        enemy_group.add(enemy)
        timer = 160 * 2


    write_info()
    #ეკრანის განახლება
    pygame.display.update()

    # pygame.sprite.groupcollide(bullet_group, enemy_group)
    if score < missed:
        run = False


mixer.music.stop()
game_over()
game_over_sound.play()
pygame.display.update()
pygame.time.wait(3000)

#ფაიგეიმიდან და სისტემიდან გამოსვლა
pygame.quit()
sys.exit()