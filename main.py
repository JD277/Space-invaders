from sys import exit
import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Graphics/Icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
running = True
# Background
bg = pygame.image.load('Graphics/bg.png')
# Game active
game_active = True


# Bullet Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/bullet.png')
        self.rect = self.image.get_rect(
            center=(0, 0))
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.test = -7
        self.rect.x = space_player.sprite.rect.x + 22
        self.rect.y = space_player.sprite.rect.y

    def movement(self):
        global state_bullet
        if state_bullet:
            self.rect.y += self.test

    def destroy(self):
        if self.rect <= 0:
            self.kill()

    def update(self):
        self.movement()


bullet_sprite = pygame.sprite.Group()
state_bullet = False

# Player Sprite
class SpacePlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/Player.png')
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
class Enemy(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()

        if tipo == 'alien':
            self.image = pygame.image.load('Graphics/alien.png')
            self.rect = self.image.get_rect(center=(random.randint(400, 950), random.randint(300, 500)))
            self.image = pygame.transform.rotozoom(self.image, 0, 0.15)
            self.x_pos = 3
            self.y_pos = -40

    def movements(self):
        self.rect.x += self.x_pos
        if self.rect.x >= 720:
            self.x_pos = -3
            self.rect.y -= self.y_pos
        elif self.rect.x <= 0:
            self.x_pos = 3
            self.rect.y -= self.y_pos

    def update(self):
        self.movements()


enemy = pygame.sprite.Group()
# enemy.add(Enemy('alien'))
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == enemy_timer:
            enemy.add(Enemy('alien'))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_sprite.add(Bullet())
                state_bullet = True

    if game_active:
        screen.fill('#424b5b')
        screen.blit(bg, (0, 0))
        space_player.draw(screen)
        space_player.update()

        enemy.draw(screen)
        enemy.update()

        bullet_sprite.draw(screen)
        bullet_sprite.update()
    pygame.display.update()
    clock.tick(60)
