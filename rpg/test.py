from PIL import Image
import os

# загружаем изображение
image_path = "images/entity/player/shadow.png"
image = Image.open(image_path)

# размеры одного тайла
tile_width = 16  # замените на ширину тайла
tile_height = 32  # замените на высоту тайла

# папка для сохранения тайлов
output_folder = "images/entity/player"  # замените на вашу папку
os.makedirs(output_folder, exist_ok=True)  # создаёт папку, если её ещё нет

# подсчёт рядов и колонок
rows = image.height // tile_height
cols = image.width // tile_width

# обработка каждого тайла
for col in range(cols):  # теперь сначала идёт проход по колонкам
    for row in range(rows):  # затем по рядам
        # вычисляем координаты тайла
        left = col * tile_width
        upper = row * tile_height
        right = left + tile_width
        lower = upper + tile_height

        # обрезаем тайл
        tile = image.crop((left, upper, right, lower))

        # проверяем, пустой ли тайл (все пиксели прозрачные)
        if tile.getbbox():  # getbbox() возвращает границы непустой области или None, если тайл пустой
            # сохраняем только непустые тайлы в указанную папку
            tile.save(os.path.join(output_folder, f"player_{col}_{row}.png"))