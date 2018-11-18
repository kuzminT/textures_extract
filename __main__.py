#!/usr/bin/env python

from classmodule import ConvertAtlas

# Объект с координатами, шириной и высотой
json_path = 'main_atlas.json'
img_path = 'main_atlas.png'

if __name__ == '__main__':
    ConvertAtlas(json_path, img_path)
