import json
import os, sys
from PIL import Image
import argparse


class ConvertAtlas:
    """
    :todo: Не перезаписывать существующее изображение, выдавать предупреждение?
    :todo:
    """

    def __init__(self, json_path, img_path):
        parser = argparse.ArgumentParser(description="Convert texture packer atlas of images to separate images")
        parser.add_argument('json',
                            help='path to the json configuration file')
        parser.add_argument('img',
                            help='path to the atlas image')
        args = parser.parse_args()

        if not os.path.exists(args.json):
            print('Ошибка! Файл {} не существует!'.format(args.json))
            return
        elif not os.path.exists(args.img):
            print('Ошибка! Файл изображения {} не существует!'.format(args.img))
            return

        self.json_path = args.json
        self.img_path = args.img

        with open(self.json_path) as data_file:
            data = json.load(data_file)
            self.img = Image.open(self.img_path)
            for frame_name in data['frames']:
                dir_name = os.path.dirname(frame_name)  # Получаем имя директории
                file_name = os.path.splitext(frame_name)[0]  # Получаем имя файла без расширения
                file_name = os.path.split(file_name)[-1]  # Отделение имени файла от названия директории
                img_data = data["frames"].get(frame_name)
                self.crop(img_data, dir_name, file_name)
                # cropped_img.show() # Показать изображение

    def crop(self, img_data, dir_name, file_name):

        frame = img_data.get('frame')
        # Определяем точки прямоугольника, который нужно вырезать
        left = frame.get('x')
        top = frame.get('y')
        width = frame.get('w')
        height = frame.get('h')
        right = left + width
        bottom = top + height
        area = (left, top, right, bottom)
        cropped_img = self.img.crop(area)

        if not os.path.exists('images'):
            os.mkdir('images', mode=0o775)

        if dir_name:
            dir_name = './images/{}'.format(dir_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, 0o777)
            img_path = '{dir_name}/{file_name}.png'.format(dir_name=dir_name, file_name=file_name)
        else:
            img_path = 'images/{}.png'.format(file_name)
        # print(img_path)
        cropped_img.save(img_path)  # Сохраняем всё в png-формате
        print('Image {} successfully saved'.format(img_path))
