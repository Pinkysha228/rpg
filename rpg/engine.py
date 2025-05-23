import pygame
from pytmx import load_pygame
import json
import os

pygame.init()

def CheckGameFiles():
    true_files_for_player = {
        'player_0_0.png', 'player_0_1.png', 'player_0_2.png', 'player_0_3.png', 'player_0_4.png',
        'player_0_5.png', 'player_10_3.png', 'player_10_4.png', 'player_10_5.png', 'player_1_0.png',
        'player_1_1.png', 'player_1_2.png', 'player_1_3.png', 'player_1_4.png', 'player_1_5.png',
        'player_2_0.png', 'player_2_1.png', 'player_2_2.png', 'player_2_3.png', 'player_2_4.png',
        'player_2_5.png', 'player_3_1.png', 'player_3_3.png', 'player_3_4.png', 'player_3_5.png',
        'player_4_3.png', 'player_4_4.png', 'player_4_5.png', 'player_5_3.png', 'player_5_4.png',
        'player_5_5.png', 'player_6_3.png', 'player_6_4.png', 'player_6_5.png', 'player_7_3.png',
        'player_7_4.png', 'player_7_5.png', 'player_8_3.png', 'player_8_4.png', 'player_8_5.png',
        'player_9_3.png', 'player_9_4.png', 'player_9_5.png', 'shadow.png'
    }
    directory = "images/entity/player"
    existing_files_for_player = set(os.listdir(directory))
    missing_files_for_player = true_files_for_player - existing_files_for_player
    if missing_files_for_player:
        print(f"FileNotFound for player: {missing_files_for_player}")
        surf = pygame.Surface((16, 32))
        surf.fill((0, 0, 0,))
        pygame.image.save(surf, 'images/entity/player/RPGEngine.png')
    else:
        print('Player files correct')


class Player:
    def __init__(self, hp, speed, screen):
        self.speed = speed
        self.hp = hp
        self.screen = screen
        self.direction = pygame.Vector2(0, 0)
        self.lookDirection = 'down'

        self.scale = 2

        self.load_animations()
        self.init_player()

        self.frame_index = 0
        self.fps_for_animation = 8
        self.animation_timer = 0

    def load_animations(self):
        walk_right = []
        for i in range(1, 3):
            img = pygame.image.load(f'images/entity/player/player_{i}_0.png').convert_alpha()
            img_scaled = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            walk_right.append(img_scaled)

        walk_left = [pygame.transform.flip(img, True, False) for img in walk_right]

        walk_down = []
        for i in range(0, 4):
            img = pygame.image.load(f'images/entity/player/player_{i}_1.png').convert_alpha()
            img_scaled = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            walk_down.append(img_scaled)

        walk_up = []
        for i in range(1, 3):
            img = pygame.image.load(f'images/entity/player/player_{i}_2.png').convert_alpha()
            img_scaled = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            walk_up.append(img_scaled)

        idle = []
        img = pygame.image.load(f'images/entity/player/player_0_1.png').convert_alpha()
        img_scaled = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        idle.append(img_scaled)

        self.player_animations = {
            'right': walk_right,
            'left': walk_left,
            'down': walk_down,
            'up': walk_up,
            'idle': idle
        }

    def init_player(self):
        self.player_surf = self.player_animations['idle'][0]  # <-- Додано це!
        self.player_rect = self.player_surf.get_rect(center=(400, 300))

    def show(self):
        self.screen.blit(self.player_surf, self.player_rect)

    def move(self, dt):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        self.player_rect.center += self.direction * self.speed * dt

        if self.direction.x > 0:
            self.lookDirection = 'right'
        elif self.direction.x < 0:
            self.lookDirection = 'left'
        elif self.direction.y > 0:
            self.lookDirection = 'down'
        elif self.direction.y < 0:
            self.lookDirection = 'up'
        elif self.direction.y == 0 and self.direction.x == 0:
            self.lookDirection = 'idle'

        if self.direction.length_squared() > 0:
            self.update_animation(dt)
        else:
            self.frame_index = 0
            self.player_surf = self.player_animations[self.lookDirection][0]

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= 1 / self.fps_for_animation:
            self.animation_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.player_animations[self.lookDirection]):
                self.frame_index = 0
        try:
            self.player_surf = self.player_animations[self.lookDirection][self.frame_index]
        except IndexError:
            pass

    def get_player_info(self):
        player_info = {'x': self.player_rect.centerx, 'y': self.player_rect.centery, 'player_hp': self.hp}
        return player_info
    
    def update_player_info(self, coords: list, hp: int):
        self.hp = hp
        self.player_rect.centerx = coords[0]
        self.player_rect.centery = coords[1]

class World:
    def __init__(self, map, screen, player):
        self.map = map
        self.screen = screen
        self.tmx_data = None
        self.player = player
        self.save = None

    def load_world(self):
        self.tmx_data = load_pygame(self.map)
    
    def update_world(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, image in layer.tiles():
                    self.screen.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def save_world(self, player_info):
        self.save = {'player_dir_x': player_info['x'],
            'player_dir_y': player_info['y'],
            'player_hp': player_info['player_hp']}
        print(self.save)
        with open('save.json', 'w') as file:
            json.dump(self.save, file, indent=4)

    def load_world_save(self):
        try:
            with open('save.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.save_world({'x': 0, 'y': 0, 'hp': 100})

        try:
            print(data)
        except UnboundLocalError:
            print('UnboundLocalError')
        return data
