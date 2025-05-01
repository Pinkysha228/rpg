import pygame
from pytmx import load_pygame
import engine

window_size = (600, 600)

pygame.init()

screen = pygame.display.set_mode(window_size)

# player
player = engine.Player(100, speed=100, screen=screen)

# map
map = engine.World('map/map.tmx', screen, player)
map.load_world()
save = map.load_world_save()
try:
    player.update_player_info([save['x'], save['y']], save['player_hp'])
except KeyError:
    player.update_player_info([save['player_dir_x'], save['player_dir_y']], save['player_hp'])

pygame.display.set_caption("RPG")

clock = pygame.time.Clock()

running = True

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            map.save_world(player.get_player_info())
            running = False

    map.update_world()

    player.move(dt)

    player.show()

    pygame.display.flip()
    print(f"FPS: {clock.get_fps():.2f}, dt: {dt:.4f}")

pygame.quit()
