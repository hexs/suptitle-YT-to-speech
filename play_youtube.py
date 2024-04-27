from func import *
from preload_sound import video_id

with open(f'data/{video_id}/transcript.json', encoding='utf-8') as f:
    string = f.read()
transcript = json.loads(string)

with open(f'data/{video_id}/video_data.json', encoding='utf-8') as f:
    string = f.read()
video_data_dict = json.loads(string)

v = input('>>')
try:
    m, s = v.split(':')
    m = int(m)
    s = int(s)
except:
    m, s = 0, 0
print(f'{m}:{s}')
datetime_to_start = datetime.now() - timedelta(minutes=m, seconds=s)
for i in range(len(transcript)):
    if video_data_dict['subtitle_lang'] == 'en':
        if transcript[i].get('text_translate_to_th') is None:
            with open(f'data/{video_id}/transcript.json', encoding='utf-8') as f:
                string = f.read()
            transcript = json.loads(string)
        text_translate_to_th = transcript[i]['text_translate_to_th']
    start = transcript[i]['start']
    text = transcript[i]['text']

    timedelta_of_vdo = datetime.now() - datetime_to_start
    if timedelta_of_vdo.total_seconds() > start + 4:
        print(f'{RED}skip {text}{ENDC}')
        continue
    while True:
        speed = 0.6
        timedelta_of_vdo = datetime.now() - datetime_to_start
        if timedelta_of_vdo.total_seconds() > start:
            lag = timedelta_of_vdo.total_seconds() - start

            print(f'{timedelta_of_vdo} | lag{YELLOW}{round(lag)}{ENDC}')
            print(text)
            if video_data_dict['subtitle_lang'] == 'en':
                print(text_translate_to_th)
            print()
            if lag > 2:
                speed = 0.7
            play(f'data/{video_id}/mp3/{i}-{speed}.mp3')
            break
