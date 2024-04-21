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
play_dt = datetime.now() - timedelta(minutes=m, seconds=s)
for i in range(len(transcript)):
    if video_data_dict == 'en':
        if transcript[i].get('text_translate_to_th') is None:
            with open(f'data/{video_id}/transcript.json', encoding='utf-8') as f:
                string = f.read()
            transcript = json.loads(string)

        text_translate_to_th = transcript[i]['text_translate_to_th']
    start = transcript[i]['start']
    text = transcript[i]['text']

    vdo_t = datetime.now() - play_dt
    if vdo_t.total_seconds() > start + 4:
        print(f'{RED}skip {text}{ENDC}')
        continue
    while True:
        vdo_t = datetime.now() - play_dt
        if vdo_t.total_seconds() > start:
            print(f'{vdo_t} | lag{YELLOW}{round(vdo_t.total_seconds() - start)}{ENDC}')
            print(text)
            if video_data_dict == 'en':
                print(text_translate_to_th)
            print()
            play(f'data/{video_id}/mp3/{i}.mp3')
            break
