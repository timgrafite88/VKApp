import requests
from VK import VK
class YandexDisc:
    """Класс работы с Яндекс диском"""

    def __init__(self, ya_token):
        self.ya_token = ya_token

    def create_folder(self, folder_name):
        requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                     params={'path': folder_name},
                     headers={'Authorization': f'OAuth {self.ya_token}'})

    def upload_photo(self, file_url, folder_name, file_name):
        ya_params = {
            'url': file_url,
            'path': f'{folder_name}/{file_name}'
        }
        headers = {
            'Authorization': f'OAuth {self.ya_token}'
        }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                 params=ya_params,
                                 headers=headers)
