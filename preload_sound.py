import json
import os
import time
from datetime import datetime
import concurrent.futures
import func
from func import text_to_mp3, get_transcript, translator


def write_data_to_json_file(json_file_name, data):
    string = json.dumps(data, indent=4, ensure_ascii=False)
    with open(f'data/{video_id}/{json_file_name}', 'w', encoding='utf-8') as f:
        f.write(string)


def read_data_from_json_file(json_file_name):
    print(f'data/{video_id}/{json_file_name}')
    with open(f'data/{video_id}/{json_file_name}', encoding='utf-8') as f:
        string = f.read()
    data = json.loads(string)
    return data


url = 'https://www.youtube.com/watch?v=tpCFfeUEGs8&ab_channel=DanielBourke'
url = 'https://www.youtube.com/watch?v=ptkzzNaZb7U&ab_channel=MarkRober'

data_from_url = {}
for i in url.split('?')[1].split('&'):
    k, v = i.split('=')
    print(f'{k:11}: {v}')
    data_from_url[k] = v
video_id = data_from_url['v']

if __name__ == '__main__':
    use_en_to_th = False
    transcript, subtitle_lang = get_transcript(video_id, use_en_to_th)
    # print(transcript)

    if video_id not in os.listdir('data'):
        os.mkdir(f'data/{video_id}')
    if 'mp3' not in os.listdir(f'data/{video_id}'):
        os.mkdir(f'data/{video_id}/mp3')

    d = os.listdir(f'data/{video_id}')
    video_data_dict = data_from_url.copy()
    video_data_dict.update({'subtitle_lang': subtitle_lang})
    print(video_data_dict)

    write_data_to_json_file('video_data.json', video_data_dict)

    if 'transcript.json' in d:
        transcript = read_data_from_json_file('transcript.json')
    else:
        write_data_to_json_file('transcript.json', transcript)
    transcript_len = len(transcript)

    mp3_path_list = os.listdir(f'data/{video_id}/mp3')
    mp3_number_list = [int(mp3_path.split('.')[0]) for mp3_path in mp3_path_list]
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
    workers = 10


    def task(taskmod):
        # taskmod is 0 to workers
        for i in range(transcript_start + taskmod, transcript_len, workers):
            time.sleep(1)
            line = transcript[i]
            if f'{i}.mp3' in os.listdir(f'data/{video_id}/mp3/'):
                if transcript[i].get('text_translate_to_th'):
                    print(f'{i}/{transcript_len}\n', end='')
                    continue

            dt_obj = datetime.fromtimestamp(line['start'])
            dt_stamp0 = datetime.fromtimestamp(0)

            if subtitle_lang == 'en':
                line['text_translate_to_th'] = translator(line['text'])
                write_data_to_json_file('transcript.json', transcript)
            if subtitle_lang == 'th':
                line['text_translate_to_th'] = line['text']
            text_to_mp3(line['text_translate_to_th'], f"data/{video_id}/mp3/{i}")

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
