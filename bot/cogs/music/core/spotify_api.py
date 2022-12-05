import requests
import re


class Spotify_api():
    def __init__(self, client_id:str, client_secret:str) -> None:
        auth_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            }
        auth_response = requests.post(auth_url, data)           
        self.token = auth_response.json()['access_token']


    def url_to_id(self, url:str) -> str:
        url_rx = re.compile("(https?:\/\/)?(www.)?(open.spotify.com\/)?(playlist\/|track\/)")
        if url_rx.match(url):
            split_url = url.split('/')
            return [split_url[3], split_url[4].split('?')[0]]
            

    def get_tracks(self, url:str, limit:int = 10) -> str|list:
        result = self.url_to_id(url)
        if not result:
            return

        headers = {
            "Authorization": "Bearer " + self.token
        }
        
        if result[0] == 'track':
            url = f'https://api.spotify.com/v1/tracks/{result[1]}'
        else:
            url = f'https://api.spotify.com/v1/playlists/{result[1]}/tracks?fields=items(track(name%2C%20artists(name)))&limit={limit}'

        r = requests.get(url=url, headers=headers)
        res = r.json()

        if r.status_code != 200:
            return

        if result[0] == 'track':
            return [f"{res['artists'][0]['name']} {res['name']}"]
        else:
            list = []
            for item in res['items']:
                list.append(f"{item['track']['artists'][0]['name']} - {item['track']['name']}")
            return list