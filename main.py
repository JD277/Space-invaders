import math
import random
from sys import exit

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Graphics/Icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
running = True
# Background
bg = pygame.image.load('Graphics/bg.png').convert_alpha()
# Game active
game_active = True

# Score
score = 0


# Bullet Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(
            center=(0, 0))
        self.image = pygame.transform.rotozoom(self.image, 0, 0.6)
        self.test = -7
        self.rect.x = space_player.sprite.rect.x + 22
        self.rect.y = space_player.sprite.rect.y

    def movement(self):
        global state_bullet
        if state_bullet:
            self.rect.y += self.test

    def destroy(self):
        global state_bullet, score
        if state_bullet:
            if self.rect.y <= 20:
                state_bullet = False
                self.rect.y = space_player.sprite.rect.y
                self.kill()

    def update(self):
        self.movement()
        self.destroy()


bullet_sprite = pygame.sprite.GroupSingle()
state_bullet = False


# Player Sprite
class SpacePlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/Player.png').convert_alpha()
        self.rect = self.image.get_rect(center=(610, 750))
        self.image = pygame.transform.rotozoom(self.image, 0, 0.15)

    def player_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            if self.rect.x < 720:
                self.rect.x += 4

        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            if self.rect.x >= 0:
                self.rect.x -= 4

    def update(self):
        self.player_input()


space_player = pygame.sprite.GroupSingle()
space_player.add(SpacePlayer())


# Enemy Sprite
enemy_image = pygame.image.load('Graphics/alien.png').convert_alpha()
enemy_rect = enemy_image.get_rect(center=(random.randint(400, 950), random.randint(300, 500)))
enemy_image = pygame.transform.rotozoom(enemy_image, 0, 0.15)
x_pos = 3
y_pos = -40


def movements():
    global x_pos, y_pos
    enemy_rect.x += x_pos
    if enemy_rect.x >= 720:
        x_pos = -3
        enemy_rect.y -= y_pos
    elif enemy_rect.x <= 0:
        x_pos = 3
        enemy_rect.y -= y_pos


enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)


def collision_of_bullet():
    global score, state_bullet
    if state_bullet:
        t1 = bullet_sprite.sprite.rect.x
        t2 = bullet_sprite.sprite.rect.y
        t3 = enemy_rect.x
        t4 = enemy_rect.y

        distance = math.sqrt((math.pow(t3-t1, 2)) + (math.pow(t4-t2, 2)))
        if distance <= 60:
            enemy_rect.y = random.randint(50, 150)
            enemy_rect.x = random.randint(100, 700)
            state_bullet = False
            bullet_sprite.sprite.kill()
            score += 5


while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if event.type == enemy_timer:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state_bullet is False:
                bullet_sprite.add(Bullet())
                state_bullet = True

    if game_active:

        screen.blit(bg, (0, 0))
        bullet_sprite.draw(screen)
        bullet_sprite.update()
        space_player.draw(screen)
        space_player.update()

        screen.blit(enemy_image, enemy_rect)
        movements()

        collision_of_bullet()

    pygame.display.update()
    clock.tick(60)
