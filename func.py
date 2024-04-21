from datetime import datetime, timedelta
import json
import requests
import os
import time
from googletrans import Translator
from youtube_transcript_api import YouTubeTranscriptApi

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

BLACK = '\033[90m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PINK = '\033[95m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'
ITALICIZED = '\033[3m'
UNDERLINE = '\033[4m'


def replace_text(text):
    text = text.replace('...', ' ')
    text = text.replace('&#39;s', ' ')
    text = text.replace('.', ' ')
    return text


def translator(text):
    while True:
        try:
            text = replace_text(text)
            translator = Translator()
            translated = translator.translate(text, dest='th').text
            break
        except Exception as e:
            print(f'{RED}translator error \n{e}{ENDC}')
            time.sleep(10)
    return translated


def get_transcript(video_id, en=False):
    def for_en():
        try:
            lang = 'en'
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except:
            try:
                lang = 'en-US'
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('en-US',))
            except:
                x = YouTubeTranscriptApi.list_transcripts(video_id)
                print(x)
        return transcript, lang

    if en:
        return for_en()
    else:
        try:
            lang = 'th'
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('th',))
        except:
            return for_en()
    return transcript, lang

def text_to_mp3(text, path_and_name):
    text = replace_text(text)
    url = f'https://texttospeech.responsivevoice.org/v1/text:synthesize?text={text}&lang=th&engine=g1&name=&pitch=0.5&rate=0.6&volume=1&key=kvfbSITh&gender=female'
    while True:
        try:
            print(BLUE, 'download', text, ENDC)
            r = requests.get(url)
            if r.status_code == 200:
                with open(path_and_name, 'wb') as f:
                    f.write(r.content)
                break
            else:
                print(f'{YELLOW}status_code = {r.status_code}{ENDC}')
                print(f'{RED}sleep 10s{ENDC}')
                time.sleep(10)
        except Exception as e:
            print(f'{YELLOW} {e} {ENDC}')
            print(f'{RED}sleep 5s{ENDC}')
            time.sleep(5)


def play(path_and_name):
    pygame.init()
    pygame.mixer.init()
    sound1 = pygame.mixer.Sound(path_and_name)
    sound1.play()
    time.sleep(sound1.get_length() - 0.1)


if __name__ == '__main__':
    pass
