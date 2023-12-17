import pygame, random, sys
from pygame.locals import *

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode([screen_width, screen_height])

alien_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

Alien = "data/box.png"
Player = "data/tank_track.png"

CameraX = 0
CameraY = 0


def main():
    class Enemy(pygame.sprite.Sprite):

        def __init__(self, image):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load(image).convert_alpha()
            self.rect = self.image.get_rect()

        def create(self):
            for i in range(50):
                alien = Enemy(Alien)

                alien.rect.x = random.randrange(screen_width - 50 - CameraX)
                alien.rect.y = random.randrange(screen_height - 50 - CameraY)

                alien_list.add(alien)
                all_sprites.add(alien)

    player = Enemy(Player)
    all_sprites.add(player)

    done = False

    clock = pygame.time.Clock()

    score = 0

    moveCameraX = 0
    moveCameraY = 0

    player.rect.x = 476
    player.rect.y = 296

    Enemy.create()

    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if event.type == KEYDOWN:
            if event.key == K_w:
                moveCameraY = -10
            if event.key == K_s:
                moveCameraY = 10
            if event.key == K_a:
                moveCameraX = -10
            if event.key == K_d:
                moveCameraX = 10

        if event.type == KEYUP:
            if event.key == K_w:
                moveCameraY = 0
            if event.key == K_s:
                moveCameraY = 0
            if event.key == K_a:
                moveCameraX = 0
            if event.key == K_d:
                moveCameraX = 0

        screen.fill(white)

        enemys_hit = pygame.sprite.spritecollide(player, alien_list, True)

        for enemy in enemys_hit:
            score += 1
            print(score)

        all_sprites.draw(screen)

        clock.tick(40)

        pygame.display.flip()

    pygame.quit()
