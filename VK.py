import requests
from tqdm import tqdm
import json
from datetime import datetime


class VK:
    """Класс работы с ВК"""

    def __init__(self, token):
        self.token = token

    def get_params(self):
        return {
            'access_token': self.token,
            'v': '5.199',
            'extended': '1',
            'album_id': 'profile'
        }

    def get_user_params(self):
        """Функция получения от пользователя количества сохраняемых фотографий"""

        photo_count = input('Какое количество фотогрфий будем сохранять на Яндекс-Диск? ')
        return photo_count

    def get_photos(self, count=5):
        """Получение массива данных из ВК"""
        vk_url = 'https://api.vk.com/method/photos.get'
        response_vk = requests.get(vk_url, params=self.get_params())
        try:
            dict_photos = response_vk.json()['response']
            photos = dict_photos['items'][:count]
            return photos
        except:
            return 'Что-то не так с токеном!'