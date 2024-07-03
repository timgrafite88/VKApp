import requests
from tqdm import tqdm
import json

vk_token = input('Введите свой ВК-токен: ')
ya_token = input('Введите свой токен от Яндекс-диска: ')

#параметры ВК
vk_params = {'access_token' : vk_token,
                'v' : '5.199',
                'extended' : '1',
                'album_id' : 'profile'}

#Основной URL VK
vk_url = 'https://api.vk.ru/method/photos.get'

response_vk = requests.get(vk_url, params = vk_params)

photo_cnt = response_vk.json()['response']['count']
dict_fotos = response_vk.json()['response']

#значение по умолчанию - сколько скачиваем фотографий
default_cnt = 5

# получаем список словарей из имя файла(количество лайков фото) и ссылка на фото максимального размера

max_foto_list = []
dict_info = []

for i in tqdm(range(default_cnt)):
    photos = dict_fotos['items'][i]['sizes']
    max_size = 0
    idx_max_size = 0
    for k, photo in enumerate(photos):
        if (photo['width'] * photo['height']) > max_size:
            max_size = photo['width'] * photo['height']
            idx_max_size = k

    # сохраняем лайки в переменную
    like_count = response_vk.json()['response']['items'][i]['likes']['count']

    # заполняем список словарей с фотографиями
    max_foto_list.append({like_count: photos[idx_max_size]['url']})

    # заполняем список словарей с информацией по фотографиям
    dict_info.append({'file_name': f'{like_count}.jpeg', 'size': photos[idx_max_size]['type']})


#создание папки на Яндекс диске для загрузки фото
folder_name = input('Введите имя папки, которая будет создана на Яндекс диске: ')

requests.put('https://cloud-api.yandex.net/v1/disk/resources',
             params={'path': folder_name},
             headers={'Authorization': f'OAuth {ya_token}'})

# скачивание фото на Яндекс диск
for info in tqdm(max_foto_list):
    for file_name, file_url in info.items():
        try:

            ya_params = {
                'url': file_url,
                'path': f'{folder_name}/{file_name}'
            }

            headers = {
                'Authorization': f'OAuth {ya_token}'
            }

            response = requests.post(f'https://cloud-api.yandex.net/v1/disk/resources/upload',
                                     params=ya_params,
                                     headers=headers)

        except:
            print('Что-то пошло не так')


#json-ы с информацией по скачанным фото
[json.dumps(info) for info in dict_info]