import requests
from tqdm import tqdm
import json
from datetime import datetime


class VK:
    """Класс работы с ВК"""

    def __init__(self, vk_token):
        self.vk_token = vk_token
        self.vk_user = input('Введите ID или screen_name: ')

    def get_vk_req(self):
        """Функция получения ответа от ВК"""
        vk_user = 'https://api.vk.ru/method/users.get'
        user_params = {'access_token': self.vk_token,
                       'user_ids': f'{self.vk_user}',
                       'v': '5.199'
                       }
        return requests.get(vk_user, params=user_params).json()

    def get_params(self):
        # параметры подключения
        return {
            'access_token': self.vk_token,
            'user_id': self.get_vk_id(),
            'v': '5.199',
            'extended': '1',
            'album_id': 'profile'
        }

    def get_count_user_photo(self):
        """Функция возвращает количество фотографий в профиле ВК пользователя"""
        res = self.get_vk_info()
        return res['count']

    def get_vk_id(self):
        """Функция получения id пользователя"""
        res = self.get_vk_req()
        return str(res['response'][0]['id'])

    def get_vk_info(self):
        """Функция получения информации о пользователе"""
        vk_url = 'https://api.vk.ru/method/photos.get'
        response_vk = requests.get(vk_url, params=self.get_params())
        dict_fotos = response_vk.json()['response']
        return dict_fotos

    def get_user_params(self):
        """Функция получения от пользователя количества сохраняемых фотографий"""
        photo_count = input(
            f'Какое количество фотогрфий будем сохранять на Яндекс-Диск? От 0 до {self.get_count_user_photo()} ')
        return int(photo_count)

    def get_users_photo_info(self):
        """Функция получения информации о фотографиях пользователя"""
        cnt = self.get_user_params()
        max_foto_list = []

        try:
            dict_fotos = self.get_vk_info()
            try:
                for i in tqdm(range(cnt)):
                    photos = dict_fotos['items'][i]['sizes']
                    max_size = 0
                    idx_max_size = 0
                    for k, photo in enumerate(photos):
                        if photo['width'] * photo['height'] == 0:
                            continue
                        elif (photo['width'] * photo['height']) > max_size:
                            max_size = photo['width'] * photo['height']
                            idx_max_size = k

                    # сохраняем лайки в переменную
                    like_count = dict_fotos['items'][i]['likes']['count']

                    # заполняем список словарей с фотографиями
                    max_foto_list.append({'likes': like_count,
                                          'url': photos[idx_max_size]['url'],
                                          'size': photos[idx_max_size]['type'],
                                          'date': datetime.utcfromtimestamp(dict_fotos['items'][i]['date']).strftime(
                                              "%d_%m_%Y")})
            except:
                return 'У пользователя нет столько фотографий в профиле!'

        except:
            return 'Возникла какая-то ошибка. Возможно целевой профиль является приватным!'

        return max_foto_list