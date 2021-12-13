import os
import glob
import json
import random
from contextlib import suppress

from models.Intent import IntentClassifier
from features.Lights import LightStrip, SmartPlugs
from features.Chat import ChatHandler
from features.Eyes import Camera

class Bot(ChatHandler):

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        report = {
              'Classifier': 'Inactive',
              'LightStrip': 'Inactive',
              'SmartPlugs': 'Inactive',
              'Answers':'Inactive',
              'Camera': 'Inactive'
              }
        with suppress(Exception):
            # Load intent model
            self.model = IntentClassifier()
            report['Classifier'] = 'Active'
        with suppress(Exception):
            # Load light strip
            self.lightstip = LightStrip()
            report['LightStrip'] = 'Active'
        with suppress(Exception):
            # Load smart plugs
            self.smart_plugs = SmartPlugs()
            report['SmartPlugs'] = 'Active'
        with suppress(Exception):
            # Load answers
            self.answers = self.load_answers()
            report['Answers'] = 'Active'
        with suppress(Exception):
            # Load PiCamera
            self.camera = Camera()
            report['Camera'] = 'Active'

        for key in report.keys():
            msg = '{feature}: {status}'.format(feature=key, status=report[key])
            self.send_message(self.admin, msg)

    def initialize(self):
        # Check latest message data
        last_update = self.get_last_update()
        last_update = last_update['update_id'] if last_update else 0
        # Notify the bot is ready.
        self.send_message(self.admin, 'The system is up and running.')
        # Start receiving messages
        while True:
            result = self.get_updates(offset=last_update+1, timeout=60)
            if result:
                id = str(result[0]['message']['chat']['id'])
                name = result[0]['message']['chat']['first_name']
                txt = result[0]['message']['text']
                last_update = result[0]['update_id']
                recipient, reply, media = self.evaluate(id, name, txt)
                self.send_message(recipient, reply.\
                        format(name=name, score=self.model.scores[0]))
                if media:
                    file_path = glob.glob('../{}/*'.format(media))[0]
                    if media == 'img':
                        self.send_photo(recipient, file_path)
                    else:
                        self.send_video(recipient, file_path)

    def evaluate(self, id: str, name: str, txt: str):
        if id == self.admin:
            pred = self.model.predict([txt])
            reply, media = self.execute(pred)
            return id, reply, media
        elif id == self.guest:
            self.guest_info(name, txt)
            reply = random.choice(self.answers['1'])
            return id, reply, None
        else:
            return self.admin,\
            'Someone with id {} named {} made contact with me: {}'\
                      .format(id, name, txt), None

    def execute(self, action: str):
        response = False
        media = None
        # Perform action
        if action == '0':
            with suppress(Exception):
                self.reset()
                response = True
        elif action == '1':
            response = True
            pass
        elif action == '2':
            with suppress(Exception):
                self.lightstip.turn_on()
                response = True
        elif action == '3':
            with suppress(Exception):
                self.lightstip.turn_off()
                response = True
        elif action == '4':
            with suppress(Exception):
                self.smart_plugs.devices['Lamp-1'].turn_on()
                self.smart_plugs.devices['Lamp-2'].turn_on()
                response = True
        elif action == '5':
            with suppress(Exception):
                self.smart_plugs.devices['Lamp-1'].turn_off()
                self.smart_plugs.devices['Lamp-2'].turn_off()
                response = True
        elif action == '6':
            with suppress(Exception):
                self.lightstip.turn_off()
                self.smart_plugs.devices['Lamp-1'].turn_off()
                self.smart_plugs.devices['Lamp-2'].turn_off()
                response = True
        elif action == '7':
            response = True
            pass
        elif action == '8':
            with suppress(Exception):
                self.camera.take_photo()
                response = True
                media = 'img'
        elif action == '9':
            with suppress(Exception):
                self.camera.shoot_video()
                response = True
                media = 'video'

        # Generate message based on action
        if response:
            reply = random.choice(self.answers[action])
        else:
            reply = "I'm sorry, {name}. It looks like something went wrong..."
        return reply, media

    def guest_info(self, name, txt):
        message = '{name} messaged me: {txt}'.format(name=name, txt=txt)
        self.send_message(self.admin, message)

    def load_answers(self):
        with open('../data/answers.json') as json_file:
            answers = json.load(json_file)
        return answers
