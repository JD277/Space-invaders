import math
from sys import exit
import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Graphics/Icon.png').convert_alpha()

pygame.display.set_icon(icon)

clock = pygame.time.Clock()
running = True

# Game active
game_active = False

# Background
bg = pygame.image.load('Graphics/bg.png').convert_alpha()

# score
score = 0

# font
font = pygame.font.Font('Fonts/Origin.ttf', 40)
font2 = pygame.font.Font('Fonts/Origin.ttf', 30)
space_invaders = font.render('Space invaders', False, '#5ab8a2')
space_invaders_rect = space_invaders.get_rect(center=(400, 100))


Instruction = font2.render("Press 'space' to start the game", False, '#5ab8a2')
Instruction_rect = Instruction.get_rect(center=(400, 500))


space_img = pygame.image.load('Graphics/Icon.png')
space_img = pygame.transform.rotozoom(space_img, 0, 0.6)
space_img_rect = space_img.get_rect(center=(400, 300))


def display_score():
    score_value2 = score
    score_text = font.render('Score:  ' + str(score_value2), False, '#ffffff')
    score_text_rect = score_text.get_rect(midtop=(100, 20))

    if game_active:
        screen.blit(score_text, score_text_rect)
    else:
        game_over = font2.render("Game over, your score was  " + str(score), False, '#e73626')
        game_over_rect = game_over.get_rect(center=(400, 500))
        screen.blit(game_over, game_over_rect)

    return score_value2


# Bullet Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/bullet.png').convert_alpha()
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
        global state_bullet
        if state_bullet:
            if self.rect.y <= 20:
                self.kill()
                state_bullet = False

    def update(self):
        self.movement()
        self.destroy()


# Player Sprite
class SpacePlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/Player.png').convert_alpha()
        self.rect = self.image.get_rect(center=(610, 750))
        self.rect.x = 400
        self.rect.y = 500
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


# Enemy Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        if tipo == 'alien':
            self.image = pygame.image.load('Graphics/alien.png').convert_alpha()
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

    def destroy(self):
        global state_bullet, score
        if state_bullet and enemy.sprites():
            enemy_sprite = pygame.sprite.spritecollideany(bullet_sprite.sprite, enemy)
            if enemy_sprite:
                t1 = self.rect.x - 22
                t2 = self.rect.y
                t3 = bullet_sprite.sprite.rect.x
                t4 = bullet_sprite.sprite.rect.y
                distance = math.sqrt((math.pow(t1 - t3, 2)) + (math.pow(t2 - t4, 2)))
                if distance <= 80:
                    y_pos = space_player.sprite.rect.y
                    bullet_sprite.sprite.rect.y = y_pos
                    state_bullet = False
                    bullet_sprite.sprite.kill()
                    self.kill()
                    score += 1


    def player_collision(self):
        global game_active
        if game_active:
            if enemy.sprites():
                enemy_sprite = pygame.sprite.spritecollideany(space_player.sprite, enemy)
                if enemy_sprite:
                    t1 = self.rect.x - 22
                    t2 = self.rect.y
                    t3 = space_player.sprite.rect.x
                    t4 = space_player.sprite.rect.y
                    distance = math.sqrt((math.pow(t1 - t3, 2)) + (math.pow(t2 - t4, 2)))
                    if distance <= 80:
                        game_active = False
                        enemy.empty()

    def update(self):
        self.movements()
        self.destroy()
        self.player_collision()


space_player = pygame.sprite.GroupSingle()
space_player.add(SpacePlayer())

bullet_sprite = pygame.sprite.GroupSingle()
state_bullet = False

enemy = pygame.sprite.AbstractGroup()
enemy.add(Enemy('alien'))

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

# Sounds
bg_sound = pygame.mixer.Sound('Sound/The_strokes.mp3')
bg_sound.set_volume(0.2)
bg_sound.play()

# bullet_sound = pygame.mixer.Sound()
# game_over_sound = pygame.mixer.Sound()
# shot_sound = pygame.mixer.Sound()

while running:
    # event
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == enemy_timer:
            obstacles = 6
            if len(enemy.sprites()) <= obstacles:
                enemy.add(Enemy('alien'))
                if score >= 5:
                    obstacles = 9
                elif score >= 12:
                    obstacles = 15
                elif score >= 20:
                    obstacles = 20
                elif score >= 30:
                    obstacles = 24
                elif score >= 60:
                    obstacles = 30

        if event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_SPACE and state_bullet is False:
                    bullet_sprite.add(Bullet())
                    state_bullet = True
            else:
                if event.key == pygame.K_SPACE and game_active is False:
                    game_active = True
                    score = 0

    # Game
    if game_active is True:
        screen.fill('#424b5b')
        screen.blit(bg, (0, 0))

        space_player.draw(screen)
        space_player.update()

        bullet_sprite.draw(screen)
        bullet_sprite.update()

        enemy.draw(screen)
        enemy.update()
        score = display_score()

    elif game_active is False:
        screen.fill('#41425b')
        screen.blit(space_invaders, space_invaders_rect)
        screen.blit(space_img, space_img_rect)

        if score <= 0:
            screen.blit(Instruction, Instruction_rect)
        else: score = display_score()

    pygame.display.update()
    clock.tick(60)
