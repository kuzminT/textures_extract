import json
# from os import path, mkdir
import os
# os.mkdir( path, 0755 );
# os.path.dirname(path) - возвращает имя директории пути pat
from PIL import Image
json_path = 'main_atlas.json'
img_path = 'main_atlas.png'

def crop(img_data, dir_name, file_name):
    """
    :todo: Получение адреса изображения и json из командной строки
    :todo: Не перезаписывать существующее изображение
    :todo: Создание поддиректории для изображения, извлечение адреса из пути
    :param img_data:
    :param file_name:
    :return:
    """
    # Объект с координатами, шириной и высотой
    frame = img_data.get('frame')
    # Определяем точки прямоугольника, который нужно вырезать
    left = frame.get('x')
    top = frame.get('y')
    width = frame.get('w')
    height = frame.get('h')
    right = left + width
    bottom = top + height
    area = (left, top, right, bottom)
    cropped_img = img.crop(area)

    if dir_name:
        dir_name = 'images/{}'.format(dir_name)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        img_path = '{dir_name}/{file_name}.png'.format(dir_name=dir_name, file_name=file_name)
    else:
        img_path = 'images/{}.png'.format(file_name)
    # print(img_path)
    cropped_img.save(img_path)  # Сохраняем всё в png-формате
    print('Image {} successfully saved'.format(img_path))

if __name__ == '__main__':
    with open(json_path) as data_file:
        data = json.load(data_file)
        img = Image.open(img_path)
        for frame_name in data['frames']:
            dir_name = os.path.dirname(frame_name)
            # print(dir_name)
            file_name = os.path.splitext(frame_name)[0]
            file_name = os.path.split(file_name)[-1]
            # print(file_name)
            img_data = data["frames"].get(frame_name)
            crop(img_data, dir_name, file_name)
            # cropped_img.show() # Показать изображение
