from sys import exit

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

        elif key[pygame.K_a] or key[pygame.K_LEFT] :
            if self.rect.x >= 0:
                self.rect.x -= 4

    def update(self):
        self.player_input()


space_player = pygame.sprite.GroupSingle()
space_player.add(SpacePlayer())

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_active:
        screen.fill('#424b5b')
        space_player.draw(screen)
        space_player.update()
    pygame.display.update()
    clock.tick(60)
