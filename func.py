from datetime import datetime, timedelta
import json
import re
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
                try:
                    subtitle_lang = 'en'
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('en-GB',))
                except:
                    x = YouTubeTranscriptApi.list_transcripts(video_id)
                    print(x)
                    0 / 0
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


def text_to_mp3_v2(text, path_and_name):
    base_url = "https://api.soundoftext.com"
    create_sound_endpoint = base_url + "/sounds"
    get_sound_endpoint = base_url + "/sounds/{}"

    payload = {
        "engine": "Google",
        "static": {
            "text": text,
            "voice": 'th-TH',
            "rate": '0.7'
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    create_sound_response = requests.post(create_sound_endpoint, headers=headers, data=json.dumps(payload))

    if create_sound_response.status_code == 200:
        sound_id = create_sound_response.json()["id"]

        get_sound_response = requests.get(get_sound_endpoint.format(sound_id))

        if get_sound_response.status_code == 200:
            sound_status = get_sound_response.json()["status"]

            if sound_status == "Done":
                sound_url = get_sound_response.json()["location"]

                speed = 0.5
                with open(f'{path_and_name}-{speed}.mp3', 'wb') as f:
                    f.write(requests.get(sound_url).content)

                return "MP3 file saved successfully."
            else:
                return "Sound creation is still pending. Please try again later."
        else:
            return "Failed to retrieve sound status."
    else:
        return "Failed to create sound."


def play(path_and_name):
    pygame.init()
    pygame.mixer.init()
    sound1 = pygame.mixer.Sound(path_and_name)
    sound1.play()
    time.sleep(sound1.get_length() - 0.4)


def get_youtube_thumbnail(video_id, save_path):
    print('get_youtube_thumbnail')
    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download thumbnail")

    return thumbnail_url


def get_youtube_video_id(youtube_url):
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_url)
    if not video_id_match:
        return None
    video_id = video_id_match.group(1)
    with open('video_id.json', 'w') as f:
        f.write(json.dumps(video_id))
    if 'thumbnail.jpg' not in os.listdir(f'static/{video_id}'):
        get_youtube_thumbnail(video_id, f'static/{video_id}/thumbnail.jpg')
    return video_id


if __name__ == '__main__':
    # translator = Translator()
    # translated = translator.translate('text', dest='th').text
    # print(translated)

    sound_url = text_to_mp3_v2('january', 'x.mp3')
    print("Sound URL:", sound_url)
