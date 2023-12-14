import os
import sys
import math
import pygame
import random

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
mouse_x, mouse_y = 0, 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)

    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)


class Camera:
    def __init__(self, x, y, attached_entity=None):
        self.x, self.y = x, y
        self.attached_entity = attached_entity

    def update(self):
        if self.attached_entity is not None:
            self.x, self.y = self.attached_entity.x, self.attached_entity.y

    def draw(self, screen, obj):
        obj.draw(screen, self.x, self.y)


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=0, health=100):
        super().__init__()
        # Положение в пространстве
        self.x, self.y = x, y
        self.direction = direction
        # Характеристики
        self.health = health


class Tank(Entity):
    def __init__(self, x, y, direction=0, health=100, speed=1.5, ai='player'):
        super().__init__(x, y, direction, health)
        self.image_track = pygame.transform.scale(load_image("tank_track.png"), (128, 128))
        self.image_turret = pygame.transform.scale(load_image("tank_turret.png"), (128, 128))
        self.turret_direction = direction
        self.speed = speed
        self.ai = ai

    def move(self, multiplier=1):
        self.x += math.cos(math.radians(self.direction)) * self.speed * multiplier
        self.y += math.sin(math.radians(self.direction)) * self.speed * multiplier

    def draw(self, screen, camera_x, camera_y):
        x = (camera_x - self.x) * -1
        y = (camera_y - self.y) * -1
        blitRotate(screen, self.image_track, (x + width // 2, y + height // 2), (64, 64),
                   self.direction * -1)
        blitRotate(screen, self.image_turret, (x + width // 2, y + height // 2), (64, 64),
                   self.direction * -1)

    def get_target(self):
        if self.ai == 'player':
            return mouse_x, mouse_y


class Box(Entity):
    def __init__(self, x, y, direction=0):
        super().__init__(x, y, direction, -1)
        self.box = pygame.transform.scale(load_image("box.png"), (128, 128))

    def draw(self, screen, camera_x, camera_y):
        x = (camera_x - self.x) * -1
        y = (camera_y - self.y) * -1
        blitRotate(screen, self.box, (x + width // 2, y + height // 2), (64, 64),
                   self.direction * -1)


if __name__ == '__main__':
    screen.fill((0, 0, 0))
    sprites = []
    for _ in range(10):
        sprites.append(Box(random.randint(-300, 300), random.randint(-300, 300)))
    tank = Tank(0, 0)
    camera = Camera(0, 0, tank)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            tank.move()
        if keys[pygame.K_s]:
            tank.move(-1)
        if keys[pygame.K_a]:
            tank.direction -= 1.5
        if keys[pygame.K_d]:
            tank.direction += 1.5

        camera.update()

        screen.fill((0, 0, 0))
        camera.draw(screen, tank)
        for sprite in sprites:
            camera.draw(screen, sprite)

        pygame.display.flip()
        clock.tick(60)
pygame.quit()
