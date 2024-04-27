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

preserve_dict = {
    'ธนาคารพลังงาน': 'power bank',
    'การเรียนรู้ของเครื่องจักร': 'Machine learning',
    'การเรียนรู้ของเครื่อง': 'Machine learning',
    'สมุดบันทึก Jupyter': 'jupyter notebook',
    'การเรียนรู้อย่างลึกซึ้ง': 'deep learning',
    'การเรียนรู้เชิงลึก': 'deep learning',
    'เครือข่ายประสาท': 'neural network',

}


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
            for phrase in preserve_dict:
                translated = translated.replace(phrase, f' {preserve_dict[phrase]} ')
            break
        except Exception as e:
            print(f'{RED}<def translator(text):> error \n{e}{ENDC}')
            time.sleep(10)
    return translated


def get_transcript(video_id, use_en_to_th=False):
    '''
    +---------------------------------------+--------------------------------------+
    | 1. th                                 | skip if auto_generated_to_th         |
    +---------------------------------------+--------------------------------------+
    | 2. en -> th                           | 1. en -> th                          |
    | 2. or automatic_creation(en) -> th    | 1. or automatic_creation(en) -> th   |
    +---------------------------------------+--------------------------------------+
    | 3. en - US -> th                      | 2. en - US -> th                     |
    +---------------------------------------+--------------------------------------+
    '''

    try:
        if use_en_to_th:
            0 / 0
        subtitle_lang = 'th'
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('th',))
    except:
        try:
            subtitle_lang = 'en'
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('en',))
        except:
            try:
                subtitle_lang = 'en'
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('en-US',))
            except:
                x = YouTubeTranscriptApi.list_transcripts(video_id)
                print(x)
                return
    return transcript, subtitle_lang


def text_to_mp3(text, path_and_name):
    text = replace_text(text)
    speeds = 0.6, 0.7
    for speed in speeds:
        url = f'https://texttospeech.responsivevoice.org/v1/text:synthesize?text={text}&lang=th&engine=g1&name=&pitch=0.5&rate={speed}&volume=1&key=kvfbSITh&gender=female'
        while True:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    with open(f'{path_and_name}-{speed}.mp3', 'wb') as f:
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
    time.sleep(sound1.get_length() - 0.4)


if __name__ == '__main__':
    pass
    translator = Translator()
    translated = translator.translate('text', dest='th').text
    print(translated)
