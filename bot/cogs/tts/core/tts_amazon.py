from typing import List
import requests


class TTSVoiceAmazon():
    def __init__(self) -> None:
        self.post_url = 'https://support.readaloud.app/ttstool/createParts'
        self.voice_msg = None
        self.voice_id = None

    async def text_to_voice(self, message:str):
        data = [{
                "voiceId": "Amazon Russian (Maxim)",
                "ssml": f"<speak version=\"1.0\" xml:lang=\"ru-RU\"><prosody volume='default' rate='medium' pitch='default'><break time='0s'/>{message}</prosody></speak>"
                }]

        r = requests.post(url=self.post_url, json=data)
        self.voice_id = r.text.replace('["','').replace('"]','')

        url = f'https://support.readaloud.app/ttstool/getParts?q={self.voice_id}&saveAs=narration.mp3'
        r = requests.get(url)
        self.voice_msg = r.content
        return r.content


    async def save(self, path:str='') -> List:
        if not self.voice_msg:
            print('Nothing to save')
        else:
            full_path = f'./{path}/{self.voice_id}.mp3'
            open(full_path,'wb').write(self.voice_msg)
            return {'path':f'./{path}/', 'name':f'{self.voice_id}.mp3'}

