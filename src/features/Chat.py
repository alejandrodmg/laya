import requests
import datetime
import os
import json
import random
from contextlib import suppress

class ChatHandler():

    def __init__(self):
        self.token = '000000000:XXXXXX-XXXXXX-XXXXXX'
        self.api_url = "https://api.telegram.org/bot{}/".format(self.token)
        self.admin = '111111111' # Telegram ID
        self.guest = '222222222'  #  Telegram ID

    def get_updates(self, offset=None, timeout=1):
        # method to call. This is called "polling"
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        content = []
        with suppress(Exception):
            resp = requests.get(self.api_url + method, params)
            # get the result of the json (first one is: 'ok', second: 'result')
            content = resp.json()['result']
        return content

    def get_last_update(self):
        get_result = self.get_updates()
        # at least 1 update
        if len(get_result) > 0:
            # get the latest
            last_update = get_result[-1]
        else:
            last_update = []
        return last_update

    def send_message(self, chat_id: str, text: str):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id: str, image_path: str, caption=''):
        files = {'photo': open(image_path, 'rb')} # /path/to/photo.png
        # two parameters, pic caption is optional
        data = {'chat_id': chat_id, 'caption': caption}
        resp = requests.post(self.api_url + 'sendPhoto', files=files, data=data)
        return resp

    def send_video(self, chat_id: str, video_path: str, caption=''):
        files = {'video': open(video_path, 'rb')} # /path/to/video.h264
        # two parameters, pic caption is optional
        data = {'chat_id': chat_id, 'caption': caption}
        resp = requests.post(self.api_url + 'sendVideo', files=files, data=data)
        return resp

    def send_voice(self, chat_id: str, voice_path: str):
        files = {'voice': open(voice_path, 'rb')} # /path/to/voice.waw/ogg
        data = {'chat_id': chat_id}
        resp = requests.post(self.api_url + 'sendVoice', files=files, data=data)
        return resp

    def send_document(self, chat_id: str, document_path: str, caption=''):
        files = {'document': open(document_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
        resp = requests.post(self.api_url + 'sendDocument', files=files, data=data)
        return resp

    def get_file(self, chat_id: str, file_name='image', extension='.jpg'):
        # this is made for photos but should be fairly easy for voice notes or videos up to 50MB
        file_id = self.get_last_update()['message']['photo'][-1]['file_id']
        url_to_file = self.api_url + 'getFile?' + 'chat_id={}'.format(self.admin) + '&file_id={}'.format(file_id)
        file_path = json.loads(requests.get(url_to_file).text)['result']['file_path']
        # Name and download the file
        # full path of the image to be stored
        local_image_path = os.path.join(os.getcwd(), file_name+extension)
        output_file = open(local_image_path,'wb')
        output_file.write(requests.get("https://api.telegram.org/file/bot{}/".format(self.token) + file_path).content)
        output_file.close()
        return output_file
