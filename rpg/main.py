import pygame
from pytmx import load_pygame
import engine

window_size = (600, 600)

pygame.init()

screen = pygame.display.set_mode(window_size)

# map
tmx_data = load_pygame("map/map.tmx")

# player
player = engine.Player('images/entity/player/player_0_1.png', hp=100, speed=100, screen=screen)
# textures

pygame.display.set_caption("RPG")

clock = pygame.time.Clock()

running = True

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, image in layer.tiles():
                screen.blit(image, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    player.move(dt)

    player.show()

    pygame.display.flip()
    print(f"FPS: {clock.get_fps():.2f}, dt: {dt:.4f}")

pygame.quit()
