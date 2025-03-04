import pygame
from random import randint, choice
import os
from sys import exit


# Functions and classes
def display_score():
    score = int(pygame.time.get_ticks() / 1000) - start_score
    score_surface = game_state_1_font.render(f"Score: {score}", False, "GREY")
    score_rectangle = score_surface.get_rect(center=(400, 75))
    window.blit(score_surface, score_rectangle)
    return score

def collision():
    global hp
    disappear = pygame.sprite.spritecollide(player.sprite, enemy_group, True)
    if disappear:
        hp -= 1
        pygame.mixer.Sound.play(damage)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_jump = pygame.transform.scale(
            pygame.image.load("Graphics/Sprites/Player Sprites/bunny_jump2.png").convert_alpha(), (85, 105))
        self.player_stand = pygame.transform.scale(
            pygame.image.load("Graphics/Sprites/Player Sprites/bunny_bow.png").convert_alpha(), (85,105))
        self.image = self.player_stand
        self.rect = self.image.get_rect(midbottom = (75, 525))
        self.gravity = 0
        self.hp = 3

    def player_animation(self):
        if self.rect.bottom < 525:
            self.image = self.player_jump
        else:
            self.image = self.player_stand

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 525:
            self.gravity -= 21.7
            pygame.mixer.Sound.play(jump_sound)

    def player_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 525: self.rect.bottom = 525
        if self.rect.bottom >= 525: self.gravity = 0

    def update(self):
        self.player_input()
        self.player_gravity()
        self.player_animation()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "dino":
            dino_walk_1 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Dino/Dino1.png").convert_alpha(), (100, 100))
            dino_walk_2 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Dino/Dino2.png").convert_alpha(), (100, 100))
            dino_walk_3 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Dino/Dino3.png").convert_alpha(), (100, 100))
            dino_walk_4 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Dino/Dino4.png").convert_alpha(), (100, 100))
            dino_walk_5 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Dino/Dino5.png").convert_alpha(), (100, 100))
            dino_walk_6 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Dino/Dino6.png").convert_alpha(), (100, 100))
            self.frames = [dino_walk_1, dino_walk_2, dino_walk_3, dino_walk_4, dino_walk_5, dino_walk_6]
            y_position = 530

        elif type == "bat":
            bat_flying_1 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Bat/Bat1.png").convert_alpha(), (80, 80))
            bat_flying_2 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Bat/Bat2.png").convert_alpha(), (80, 80))
            bat_flying_3 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Bat/Bat3.png").convert_alpha(), (80, 80))
            bat_flying_4 = pygame.transform.scale(
                pygame.image.load("Graphics/Sprites/Bat/Bat4.png").convert_alpha(), (80, 80))
            self.frames = [bat_flying_1, bat_flying_2, bat_flying_3, bat_flying_4]
            y_position = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1100, 1200), y_position))


    def enemy_animation(self):
        self.animation_index += 0.3
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.enemy_animation()
        self.rect.x -= 6
        if self.rect.right <= 0:
            self.rect.left = 800
        self.destroy()

    def destroy(self):
        if self.rect.x <= -75:
            self.kill()
        if self.rect.y <= 300:
            mouse_buttons = pygame.mouse.get_pressed(3)
            if mouse_buttons[0]:
                if self.rect.collidepoint(mouse_position):
                    pygame.mixer.Sound.play(enemy_damage)
                    self.kill()

        global hp
        if self.rect.x <= -75 and self.rect.y <= 300:
            hp -= 1
            pygame.mixer.Sound.play(damage)


# Essentials
pygame.init()
pygame.display.set_icon(pygame.image.load("Graphics/app icon.png"))
caption = "Bunny Dodger"
pygame.display.set_caption(caption)
width, height = 800, 550
window = pygame.display.set_mode((width, height))
black = (0, 0, 0)
# game_state 0 = intro, 1 = game, 2 = game over
game_state = 0
start_score = 0
hp = 3

# Sounds
selection_sound = pygame.mixer.Sound("Sounds/menu select.wav")
pygame.mixer.Sound.set_volume(selection_sound, 0.2)
damage = pygame.mixer.Sound("Sounds/damage.wav")
pygame.mixer.Sound.set_volume(damage, 0.2)
jump_sound = pygame.mixer.Sound("Sounds/jump.wav")
pygame.mixer.Sound.set_volume(jump_sound, 0.0000001)
music = pygame.mixer.Sound("Sounds/music.wav")
pygame.mixer.Sound.set_volume(music, 0.1)
enemy_damage = pygame.mixer.Sound("Sounds/enemy damage.wav")
pygame.mixer.Sound.set_volume(enemy_damage, 0.2)

pressed_key = pygame.key.get_pressed()

# Group methods
player = pygame.sprite.GroupSingle()
player.add(Player())

enemy_group = pygame.sprite.Group()


# Surfaces and rectangles
background_image = pygame.image.load(os.path.join("Graphics/Background/Forest Background.png")).convert()
background_surface = pygame.transform.scale(background_image, (width, height))

game_state_0_font = pygame.font.Font("Dogica Font/TTF/dogica.ttf", 35)
game_state_1_font = pygame.font.Font("Dogica Font/TTF/dogica.ttf", 20)
game_state_2_font = pygame.font.Font("Dogica Font/TTF/dogica.ttf", 30)


intro_surface = game_state_0_font.render("PRESS SPACE TO START", False, "BLACK")
intro_rectangle = intro_surface.get_rect(center = (400, 500))


restart_surface = game_state_2_font.render("CLICK HERE TO RESTART", False, "WHITE")
restart_rectangle = restart_surface.get_rect(center = (400, 225))
restart_surface_2 = game_state_2_font.render("CLICK HERE TO QUIT", False, "WHITE")
restart_rectangle_2 = restart_surface_2.get_rect(center = (400, 350))

# Spawn rate of enemies
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

# FPS
clock = pygame.time.Clock()
fps = 60
music.play(-1)


# Create the window
while True:
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Intro events
        if game_state == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(selection_sound)
                    game_state = 1
                    start_score = int(pygame.time.get_ticks() / 1000)

        # Game events
        if game_state == 1:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(["dino", "bat", "dino"])))


        # Game over events
        if game_state == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rectangle.collidepoint(event.pos):
                    pygame.mixer.Sound.play(selection_sound)
                    hp = 3
                    game_state = 1
                    start_score = int(pygame.time.get_ticks() / 1000)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rectangle_2.collidepoint(event.pos):
                    pygame.mixer.Sound.play(selection_sound)
                    pygame.quit()
                    exit()

    # Intro
    if game_state == 0:
        window.fill("mediumseagreen")
        window.blit(intro_surface, intro_rectangle)
        enemy_group.empty()


    # Gameplay
    if game_state == 1:
        # Background and text
        window.blit(background_surface, (0, 0))
        health_surface = game_state_1_font.render(f"Health: {hp}", False, "white")
        health_rectangle = health_surface.get_rect(topleft=(20, 20))
        window.blit(health_surface, health_rectangle)
        score = display_score()

        # Player and jumping mechanic
        player.draw(window)
        player.update()

        # Enemies
        enemy_group.draw(window)
        enemy_group.update()

        collision()
        if hp == 0:
            game_state = 2


    if game_state == 2:
        window.fill("mediumseagreen")
        window.blit(restart_surface, restart_rectangle)
        window.blit(restart_surface_2, restart_rectangle_2)
        score_surface = game_state_1_font.render(f"Your score was: {score}", False, "WHITE")
        score_rectangle = score_surface.get_rect(center = (400, 50))
        window.blit(score_surface, score_rectangle)
        enemy_group.empty()

    pygame.display.update()
    clock.tick(fps)