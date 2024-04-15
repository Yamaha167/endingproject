import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936 #1024

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Fly')

#define font
font = pygame.font.SysFont('Pixel', 60)

#define colors
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
trap_gap = 225
trap_frequency = 1500 #ms
last_trap = pygame.time.get_ticks() - trap_frequency
score = 0
pass_trap = False

#load images
bg = pygame.image.load('img/Background.png')
ground_img = pygame.image.load('img/floppyground.png')
rr_button_img = pygame.image.load('img/Restart.png')
esc_button_img = pygame.image.load('img/Exit.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    trap_group.empty()
    floppy.rect.x = 100
    floppy.rect.y = int(screen_height / 2)
    score = 0
    return score
class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/fli{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0

    def update(self):
        if flying == True:
            self.vel += 0.5
            if self.vel > 10:
                self.vel = 10
            if self.rect.bottom < 890:
                self.rect.y += int(self.vel)
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1.5)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], 180)


class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/Trap.png")
        self.rect = self.image.get_rect()
        #position 1 is from top -1 is from the bottom.
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(trap_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(trap_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0 :
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image= image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):

        action = False
        #get mouse pos
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action =True
        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

fly_group = pygame.sprite.Group()
trap_group = pygame.sprite.Group()

floppy = Fly(100, int(screen_height / 2))

fly_group.add(floppy)

rr_button = Button(screen_width // 2 - 50, screen_height // 2 - 100, rr_button_img)
esc_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, esc_button_img)

run = True
while run:
    clock.tick(fps)

    #add background
    screen.blit(bg, (0,0))

    fly_group.draw(screen)
    fly_group.update()
    trap_group.draw(screen)

    #check the score
    if len(trap_group) > 0:
        if fly_group.sprites()[0].rect.left > trap_group.sprites()[0].rect.left\
            and fly_group.sprites()[0].rect.right < trap_group.sprites()[0].rect.right\
            and pass_trap == False:
            pass_trap = True
        if pass_trap == True:
            if fly_group.sprites()[0].rect.left > trap_group.sprites()[0].rect.right:
                score += 1
                pass_trap = False

    draw_text(str(score), font, white, int(screen_width / 2) , 20)

    if pygame.sprite.groupcollide(fly_group, trap_group, False, False) or floppy.rect.top < 0:
        game_over = True

    if floppy.rect.bottom >= 800:
        game_over = True
        flying = False

    #draw and scroll background
    if game_over == False and flying == True:

        #generate new traps
        time_now = pygame.time.get_ticks()
        if time_now - last_trap > trap_frequency:
            trap_height = random.randint(-100, 100)
            btm_trap = Trap(screen_width, int(screen_height / 2) + trap_height, -1)
            top_trap = Trap(screen_width, int(screen_height / 2) + trap_height,1)
            trap_group.add(btm_trap)
            trap_group.add(top_trap)
            last_trap = time_now

        screen.blit(ground_img, (ground_scroll, 800))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 71:
            ground_scroll = 0

        trap_group.update()
    else:
        screen.blit(ground_img, (ground_scroll, 800))
        ground_scroll = 0

    if game_over == True:
        if rr_button.draw() == True:
            game_over = False
            score = reset_game()

    if game_over == True:
        if esc_button.draw() == True:
            pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()