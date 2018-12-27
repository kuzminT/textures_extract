import json
import os
from PIL import Image
import argparse


class ConvertAtlas:
    """
    :todo: Не перезаписывать существующее изображение, выдавать предупреждение?
    :todo: Получать в качестве аргумента название папки для сохранения вырезаемых картинок
    :todo: Обработка возможных ошибок - не тот формат файлов:
    """

    def __init__(self):
        parser = argparse.ArgumentParser(description="Convert texture packer atlas of images to separate images")
        parser.add_argument('img',
                            help='path to the atlas image')
        parser.add_argument('--json',
                            help='path to the json configuration file')
        # Флаг для переключения типа изображения и конфигурационного файла - поддерживает как современный формат
        # атласа, используемого в Texture Packer, так и стандартные spritesheets
        parser.add_argument('--format', '-f', default="atlas",
                            help='Which type of image used - json and atlas or old type spritesheets')

        parser.add_argument('--width', '-w', help='Width of one frame (only for spritesheets)', type=float)

        parser.add_argument('--height', help='Height of one frame (only for spritesheets)', type=float)

        parser.add_argument('--count', '-c', help='Count of frames (only for spritesheets)', type=int)

        args = parser.parse_args()
        image_format = args.format
        print(image_format)

        if not os.path.exists(args.img):
            print('Ошибка! Файл изображения {} не существует!'.format(args.img))
            return

        self.img_path = args.img

        if image_format == 'atlas':
            if not os.path.exists(args.json):
                print('Ошибка! Файл {} не существует!'.format(args.json))
                return

            self.json_path = args.json

            with open(self.json_path) as data_file:
                data = json.load(data_file)
                self.img = Image.open(self.img_path)
                if not os.path.exists('images'):
                    os.mkdir('images', mode=0o775)

                for frame_name in data['frames']:
                    dir_name = os.path.dirname(frame_name)  # Получаем имя директории
                    file_name = os.path.splitext(frame_name)[0]  # Получаем имя файла без расширения
                    file_name = os.path.split(file_name)[-1]  # Отделение имени файла от названия директории
                    img_data = data["frames"].get(frame_name)
                    self.crop(img_data, dir_name, file_name)

        elif image_format == 'sprite' or image_format == 'spritesheet':
            width = args.width
            height = args.height
            count = args.count

            if not height and width:
                height = width

            if not width or not count:
                print('Error! Spritesheets format required more atrguments: width, height and count')
            else:
                self.crop_spritesheet(width, height, count)
        else:
            print('Error! Unknown format of the image')


    def crop(self, img_data, dir_name, file_name):
        """
        Method for crop atlas of images by json data
        :param img_data:
        :param dir_name:
        :param file_name:
        :return:
        """

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
        # cropped_img.show() # Показать изображение

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

    def crop_spritesheet(self, width, height, count):

        self.img = Image.open(self.img_path)

        if not os.path.exists('images'):
            os.mkdir('images', mode=0o775)

        print(self.img.size)

        for i in range(count):
            left = width*i
            top = 0
            right = left + width
            bottom = top + height
            area = (left, top, right, bottom)
            cropped_img = self.img.crop(area)
            img_path = 'images/img-{}.png'.format(i)
            cropped_img.save(img_path)
            print('Image {} successfully saved'.format(img_path))
