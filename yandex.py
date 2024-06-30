import requests

class Yandex:
    def __init__(self, token):
        self.token = token

    #функция для создания папки загрузки на яндекс.диске пользователя

    def create_folder(self, name):
        headers = {'Authorization': f'OAuth {self.token}'}
        params_ya = {'path': {name}}
        ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        return requests.put(ya_url,
                            params=params_ya,
                            headers=headers)

