#!/usr/bin/env python3
from classmodule import ConvertAtlas

# Объект с координатами, шириной и высотой
# Для формата атласа указывается
# json_path = 'main_atlas.json'
# img_path = 'main_atlas.png'

#  Для формата старого spritesheet нужно указать
#  frameWidth: 65.6,
#  frameHeight: 65.6,
# Количество фреймов  frames count 4

if __name__ == '__main__':
    ConvertAtlas()
