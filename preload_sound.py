import json
import os
import time
from datetime import datetime
import concurrent.futures
import func
from func import text_to_mp3, text_to_mp3_v2, get_transcript, translator, get_youtube_thumbnail, get_youtube_video_id
import requests


def write_data_to_json_file(video_id, json_file_name, data):
    string = json.dumps(data, indent=4, ensure_ascii=False)
    with open(f'static/{video_id}/{json_file_name}', 'w', encoding='utf-8') as f:
        f.write(string)


def read_data_from_json_file(video_id, json_file_name):
    print(f'data/{video_id}/{json_file_name}')
    with open(f'static/{video_id}/{json_file_name}', encoding='utf-8') as f:
        string = f.read()
    data = json.loads(string)
    return data


def get_link_from_9222():
    res = requests.get('http://localhost:9222/json')
    youtube_watch_page = []
    lis = json.loads(res.text)
    for li in lis:
        if li['type'] == 'page' and 'https://www.youtube.com/watch' in li['url']:
            youtube_watch_page.append(li)

    if len(youtube_watch_page):
        print(youtube_watch_page[0]['title'])
        return youtube_watch_page[0]['url']
    return None


def main(url, use_en_to_th=True):
    '''
    :param url:
    :param use_en_to_th: Translate (en to th) with Google Translate
    :return:
    '''

    video_id = get_youtube_video_id(url)
    transcript, subtitle_lang = get_transcript(video_id, use_en_to_th)

    os.makedirs(f'static/{video_id}', exist_ok=True)
    os.makedirs(f'static/{video_id}/mp3', exist_ok=True)

    d = os.listdir(f'static/{video_id}')
    print('video_id', video_id)
    write_data_to_json_file(video_id, 'video_data.json', {
        'v': video_id,
        'subtitle_lang': subtitle_lang,
        'last_time': datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    })

    if 'transcript.json' in d:
        transcript = read_data_from_json_file(video_id, 'transcript.json')
    else:
        write_data_to_json_file(video_id, 'transcript.json', transcript)
    transcript_len = len(transcript)

    mp3_path_list = os.listdir(f'static/{video_id}/mp3')
    mp3_number_list = [int(mp3_path.split('-')[0]) for mp3_path in mp3_path_list]
    try:
        max_number = max(mp3_number_list)
        transcript_start = max_number + 1
        for i in range(max_number):
            if i in mp3_number_list:
                continue
            else:
                transcript_start = i
                break
    except:
        transcript_start = 0

    print('transcript_len', transcript_len)
    print('transcript_start', transcript_start)
    workers = 5

    def task(taskmod):
        # taskmod is 0 to workers
        for i in range(transcript_start + taskmod, transcript_len, workers):
            time.sleep(1)
            line = transcript[i]
            if f'{i}.mp3' in os.listdir(f'static/{video_id}/mp3/'):
                if transcript[i].get('text_translate_to_th'):
                    print(f'{i}/{transcript_len}\n', end='')
                    continue

            dt_obj = datetime.fromtimestamp(line['start'])
            dt_stamp0 = datetime.fromtimestamp(0)

            if subtitle_lang == 'en':
                line['text_translate_to_th'] = translator(line['text'])
                write_data_to_json_file(video_id, 'transcript.json', transcript)
            if subtitle_lang == 'th':
                line['text_translate_to_th'] = line['text']
            text_to_mp3(line['text_translate_to_th'], f"static/{video_id}/mp3/{i}")
            # text_to_mp3_v2(line['text_translate_to_th'], f"static/{video_id}/mp3/{i}")
            print(
                f"{i}/{transcript_len} {dt_obj - dt_stamp0}\n"
                f"{line['text']}\n"
                f"{line['text_translate_to_th']}\n"
                f"\n"
                , end=''
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for i in range(workers):
            executor.submit(task, i)  # i is   0 to workers-1

    print(f'{func.GREEN}ok{func.ENDC}')


if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=tpCFfeUEGs8&ab_channel=DanielBourke'
    # url = 'https://www.youtube.com/watch?v=fNk_zzaMoSs&ab_channel=3Blue1Brown'
    url = 'https://www.youtube.com/watch?v=Kz6IlDCyOUY&ab_channel=pixegami'
    # url = 'https://www.youtube.com/watch?v=tep1JZmDCvQ&ab_channel=THESECRETSAUCE'
    url = get_link_from_9222()
    main(url)
