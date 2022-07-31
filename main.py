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
# bg = pygame.image.load('Graphics')
# Game active
game_active = True


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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()

        if tipo == 'alien':
            self.x_pos = 3
            self.y_pos = -40
            self.image = pygame.image.load('Graphics/alien.png')
            self.rect = self.image.get_rect(center=(random.randint(250, 950), random.randint(300, 500)))
            self.image = pygame.transform.rotozoom(self.image, 0, 0.15)

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
enemy.add(Enemy('alien'))
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)


while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == enemy_timer:
        # enemy.add(Enemy('alien'))
    if game_active:
        screen.fill('#424b5b')
        space_player.draw(screen)
        space_player.update()

        enemy.draw(screen)
        enemy.update()
    pygame.display.update()
    clock.tick(60)
