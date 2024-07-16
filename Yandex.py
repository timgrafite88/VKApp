import requests
import json
from tqdm import tqdm
import configparser


class YandexDisc(VK):
    """Класс работы с Яндекс диском"""

    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.folder = input('Введите имя создаваемой папки, в которую будем сохранять фотографии: ')

    def create_folder(self):
        """Функция создания папки на Яндекс Диске"""
        requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                     params={'path': self.folder},
                     headers={'Authorization': f'OAuth {self.ya_token}'})

    def upload_photo(self):
        """Функция загрузки фотографий на диск и получения json-файлов с информацией по ним"""

        # cоздаем клиента ВК
        config = configparser.ConfigParser()  # создаём объекта парсера
        config.read("settings.ini")  # читаем конфиг
        vk_token = config["TOKENS"]["vk_token"]
        vk_client = VK(vk_token)

        info = vk_client.get_users_photo_info()  # получаем данные из ВК
        self.create_folder()  # создаем папку
        append_list = []
        info_list = []

        for info in tqdm(info):
            try:

                if info['likes'] not in append_list:
                    requests.post(f'https://cloud-api.yandex.net/v1/disk/resources/upload',
                                  params={'url': info['url'],
                                          'path': f"{self.folder}/{info['likes']}"},

                                  headers={'Authorization': f'OAuth {self.ya_token}'})

                    append_list.append(info['likes'])

                    info_list.append({
                        'file_name': f"{info['likes']}.jpeg",
                        'size': info['size']
                    })

                else:
                    requests.post(f'https://cloud-api.yandex.net/v1/disk/resources/upload',
                                  params={'url': info['url'],
                                          'path': f"{self.folder}/{info['likes']}_{info['date']}"},

                                  headers={'Authorization': f'OAuth {self.ya_token}'})

                    info_list.append({
                        'file_name': f"{info['likes']}_{info['date']}.jpeg",
                        'size': info['size']
                    })


            except:
                print('Что-то пошло не так')

        return [json.dumps(info) for info in info_list]


if main != "main":
    pass
else:
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    ya_token = config["TOKENS"]["ya_token"]

    ya = YandexDisc(ya_token)
    ya.upload_photo()