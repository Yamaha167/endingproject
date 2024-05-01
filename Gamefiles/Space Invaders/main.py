import pygame
from pygame.locals import *
import random
from pygame import mixer
import asyncio

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

screen_width = 600
screen_height = 766

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Home Invaderz')

#define fonts
font30 = pygame.font.SysFont('constantia', 30)
font40 = pygame.font.SysFont('constantia', 40)
async def main():
    #load sounds
    explosion_fx = pygame.mixer.Sound('image/explosion.wav')
    explosion_fx.set_volume(0.25)

    laser_fx = pygame.mixer.Sound('image/Pew.wav')
    laser_fx.set_volume(0.25)


    #game vars.

    rows = 5
    cols = 5
    bug_cooldown = 1000 #ms
    last_bug_shot = pygame.time.get_ticks()
    countdown = 3
    last_count = pygame.time.get_ticks()
    game_over = 0 #0 no game over, 1 = win, -1 - loss



    #define colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)

    bg = pygame.image.load('image/bg.png')

    #define function for creating text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))

    def draw_bg():
        screen.blit(bg, (0, 0))

    #spaceship class (child of pygame sprite class).
    class Spaceship(pygame.sprite.Sprite):
        def __init__(self, x, y, health):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('image/fingy2.png')
            self.rect = self.image.get_rect()
            self.rect.center = [x ,y]
            self.health_start = health
            self.health_remaining = health
            self.last_shot = pygame.time.get_ticks()

        def update(self):
            speed = 8

            cooldown = 400
            game_over = 0

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += speed
            #record current time
            time_now = pygame.time.get_ticks()

            #shoot
            if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)
                laser_fx.play()
                self.last_shot = time_now

            #update mask
            self.mask = pygame.mask.from_surface(self.image)

            #draw health bar
            pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 5), self.rect.width, 15))
            if self.health_remaining > 0:
                pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 5), int(self.rect.width *(self.health_remaining/self.health_start)), 15))
            elif self.health_remaining <= 0:
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                explosion_fx.play()
                explosion_group.add(explosion)
                self.kill()
                game_over = -1
            return game_over



    class Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('image/fire.png')
            self.rect = self.image.get_rect()
            self.rect.center = [x ,y]

        def update(self):
            self.rect.y -= 5
            if self.rect.bottom < 0:
                self.kill()
            if pygame.sprite.spritecollide(self, bug_group, True):
                self.kill()
                explosion_fx.play()
                explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
                explosion_group.add(explosion)


    class Bugs(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('image/' + str(random.randint(1,3)) + ".png")
            self.rect = self.image.get_rect()
            self.rect.center = [x ,y]
            self.move_counter = 0
            self.move_direction = 1

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 75:
                self.move_direction *= -1
                self.move_counter *= self.move_direction

    class BugBullets(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('image/bugbullet.png')
            self.rect = self.image.get_rect()
            self.rect.center = [x ,y]

        def update(self):
            self.rect.y += 5
            if self.rect.top > screen_height:
                self.kill()
            if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
                spaceship.health_remaining -= 1
                self.kill()
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                explosion_group.add(explosion)

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y, size):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            for num in range(1, 6):
                img = pygame.image.load(f'image/exp{num}.png')
                if size == 1:
                    img = pygame.transform.scale(img, (20, 20))
                if size == 2:
                    img = pygame.transform.scale(img, (40, 40))
                if size == 3:
                    img = pygame.transform.scale(img, (100, 100))
                self.images.append(img)
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x ,y]
            self.counter = 0

        def update(self):
            explosion_speed = 3
            #update exp animation
            self.counter += 1

            if self.counter >= explosion_speed and self.index < len(self.images) -1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]

            if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
                self.kill()
    #GROUPS --------:

    #sprite groups
    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    bug_group = pygame.sprite.Group()
    bug_bullet_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()

    def spawn_bugs():
        #spawn_enemies
        for row in range(rows):
            for item in range(cols):
                bug = Bugs(100 + item * 100, 100 + row * 70)
                bug_group.add(bug)

    spawn_bugs()



    spaceship = Spaceship(int(screen_width/2), screen_height - 100, 3)
    spaceship_group.add(spaceship)



    run = True
    while run:

        clock.tick(60)
        draw_bg()

        if countdown == 0:

            #create random bug bullets
            time_now = pygame.time.get_ticks()

            if time_now - last_bug_shot > bug_cooldown and len(bug_bullet_group) < 6 and len(bug_group) > 0:
                attacking_bug = random.choice(bug_group.sprites())
                bug_bullet = BugBullets(attacking_bug.rect.centerx, attacking_bug.rect.bottom)
                bug_bullet_group.add(bug_bullet)
                last_bug_shot = time_now

            if len(bug_group) == 0:
                game_over = 1

            if game_over == 0:
                #update spaceship.
                game_over = spaceship.update()

                #update sprite groups
                bullet_group.update()
                bug_group.update()
                bug_bullet_group.update()
            else:
                if game_over == -1:
                    draw_text('GAME OVER!', font40, red, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
                if game_over == 1:
                    draw_text('YOU WIN!', font40, green, int(screen_width / 2 - 100), int(screen_height / 2 + 50))


        if countdown > 0:
            draw_text('GET READY!', font40, white, int(screen_width/ 2 - 110), int(screen_height / 2 +50))
            draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

        #update explosion group
        explosion_group.update()

        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        bug_group.draw(screen)
        bug_bullet_group.draw(screen)
        explosion_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())