import requests
import json
from tqdm import tqdm
from VK import VK

class YandexDisc(VK):
    """Класс работы с Яндекс диском"""

    def __init__(self, ya_token):
        super.__init__(ya_token)

    def get_user_folder_name(self):
        """Функция запроса имени создаваемой папки у пользователя"""
        folder = input('Введите имя создаваемой папки, в которую будем сохранять фотографии: ')
        return folder

    def create_folder(self):
        requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                     params = {'path': self.get_user_folder_name()},
                     headers = {'Authorization': f'OAuth {self.ya_token}'})

    def upload_photo(self):
        """Функция загрузки фотографий на диск и получения json-файлов с информацией по ним"""
        info = self.get_users_photo_info()
        folder_name = self.get_user_folder_name()
        append_list = []
        info_list = []

        for info in tqdm(info):
            try:

                if info['likes'] not in append_list:
                    requests.post(f'https://cloud-api.yandex.net/v1/disk/resources/upload',
                                  params = {'url': info['url'],
                                          'path': f"{folder_name}/{info['likes']}"},

                                  headers = {'Authorization': f'OAuth {self.ya_token}'})

                    append_list.append(info['likes'])

                    info_list.append({
                        'file_name': f"{info['likes']}.jpeg",
                        'size': info['size']
                    })

                else:
                    requests.post(f'https://cloud-api.yandex.net/v1/disk/resources/upload',
                                  params = {'url': info['url'],
                                            'path': f"{folder_name}/{info['likes']}_{info['date']}"},

                                  headers = {'Authorization': f'OAuth {self.ya_token}'})

                    info_list.append({
                        'file_name': f"{info['likes']}_{info['date']}.jpeg",
                        'size': info['size']
                    })


            except:
                print('Что-то пошло не так')

        return [json.dumps(info) for info in info_list]