from func import *
from preload_sound import video_id

with open(f'data/{video_id}/video_data.json') as f:
    data_dict = json.loads(f.read())
transcript = data_dict['transcript']

v = input('>>')
try:
    m, s = v.split('.')
    m = int(m)
    s = int(s)
except:
    m, s = 0, 0
print(f'{m}:{s}')
play_dt = datetime.now() - timedelta(minutes=m, seconds=s)
for i, line in enumerate(transcript):
    start = line['start']
    text = line['text']
    vdo_t = datetime.now() - play_dt
    if vdo_t.total_seconds() > start + 4:
        print(f'{RED}skip {text}{ENDC}')
        continue
    while True:
        vdo_t = datetime.now() - play_dt
        if vdo_t.total_seconds() > start:
            print(f'{vdo_t} | lag{YELLOW}{round(vdo_t.total_seconds() - start)}{ENDC}')
            print(text)
            play(f'data/{video_id}/mp3/{i}.mp3')
            break
