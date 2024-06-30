import requests
from tqdm import tqdm
class VKAPIClient:
    BASE_URL = f'https://api.vk.ru/method'
    def __init__(self, token, user_id):

        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {'access_token' : self.token,
                'v' : '5.199',
                'extend' : '1'}

    def get_photos(self):
        params = self.get_common_params()
        response = requests.get(f'{self.BASE_URL}/photos.get', params = params)
        return response.json()