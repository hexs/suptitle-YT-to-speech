import json
from datetime import datetime, timedelta
from func import text_to_mp3, play, get_transcript, translator
import os

url = 'https://www.youtube.com/watch?v=tpCFfeUEGs8&ab_channel=DanielBourke'

url = 'https://www.youtube.com/watch?v=1j1kAuqePJo&ab_channel=CrunchLabs'

data_dict = {}
for i in url.split('?')[1].split('&'):
    k, v = i.split('=')
    print(f'{k:11}: {v}')
    data_dict[k] = v
video_id = data_dict['v']

if __name__ == '__main__':
    en = False
    transcript, lang = get_transcript(video_id, en)
    print(transcript)
    data_dict['lang'] = lang
    data_dict['transcript'] = transcript
    if video_id not in os.listdir('data'):
        os.mkdir(f'data/{video_id}')
    if 'mp3' not in os.listdir(f'data/{video_id}'):
        os.mkdir(f'data/{video_id}/mp3')

    with open(f'data/{video_id}/video_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_dict, indent=4))

    for i, line in enumerate(data_dict['transcript']):
        start = line['start']
        text = line['text']
        dt_obj = datetime.fromtimestamp(start)
        dt_stamp0 = datetime.fromtimestamp(0)
        print(dt_obj - dt_stamp0)
        print(text)

        if f'{i}.mp3' in os.listdir(f'data/{video_id}/mp3/'):
            continue
        if data_dict['lang'] == 'en':
            line['text_th'] = translator(text)
            text_to_mp3(line['text_th'], f"data/{data_dict['v']}/mp3/{i}.mp3")
        if data_dict['lang'] == 'th':
            text_to_mp3(line['text'], f"data/{data_dict['v']}/mp3/{i}.mp3")
        print()
