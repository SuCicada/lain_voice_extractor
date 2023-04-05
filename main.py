import datetime

import ass
from ass import Dialogue

# Open the ASS file

# Access the subtitle events
import os

from tqdm import tqdm

ass_map = {}


def init_ass_map():
    search_path = os.path.join(os.path.dirname(__file__), 'lainass')
    for root, dir, files in os.walk(search_path):
        for file in files:
            name = os.path.splitext(file)[0]
            path = os.path.join(root, file)
            ass_map[name] = path


def find_ass(name):
    return ass_map.get(name)


# def get_lain_event(name):
#     file = find_ass(name)
def get_lain_event(file):
    print(f"start parse lain event: {file}")
    with open(f'{file}', encoding='utf-8-sig') as f:
        doc = ass.parse(f)
    lain_event = []
    for event in doc.events:
        event: Dialogue = event
        # print(event.name)
        # print(event.start, event.end)
        if event.name == 'Lain':
            # lain_event.append((event.name, event.start, event.end, event.text))
            lain_event.append(event)
    return lain_event


import wget


def get_mp4(name, output_dir):
    url = f"https://laingame.net/media/{name}.mp4"
    output = os.path.join(output_dir, f"{name}.mp4")
    if os.path.exists(output):
        print(f"{output} exists, skip")
    else:
        print(f"start download: {url} -> {output}")
        res = wget.download(url, output)
        print(res)
    return output


from moviepy.video.io.VideoFileClip import VideoFileClip


def get_audio(mp4, output_dir):
    # def get_audio(name, mp4_dir):
    # Load the video clip
    name = os.path.splitext(os.path.basename(mp4))[0]
    tmp = f"{output_dir}/{name}.mp3"
    if not os.path.exists(tmp):
        print(f"start extract audio: {mp4} -> {tmp}")
        clip = VideoFileClip(mp4)
        # Extract the audio and save it to a file
        clip.audio.write_audiofile(tmp)
    return tmp


def cut_audio(mp3, event: Dialogue, output):
    if os.path.exists(output):
        print(f"{output} exists, skip")
        return output

    from pydub import AudioSegment
    audio_file = AudioSegment.from_file(mp3, format="mp3")

    # Set the start and end times in milliseconds
    start: datetime.timedelta = event.start
    start_time = start.total_seconds() * 1000
    end_time = event.end.total_seconds() * 1000
    print(f"cut {output}. {start_time} --> {end_time}.", end=' ')

    # Extract the segment between start and end time
    extracted_audio = audio_file[start_time:end_time]
    # Export the extracted segment as a new mp3 file
    # Load d_audio.export("output.mp3", format="mp3")
    extracted_audio.export(output, format="mp3")
    # print(res)
    print("done")
    return output


def mp3_to_wav(mp3, output_dir):
    output = os.path.join(output_dir, os.path.splitext(os.path.basename(mp3))[0] + '.wav')
    print(f"{mp3} -> {output}: ", end="")
    if os.path.exists(output):
        print("exists, skip")
    else:
        from pydub import AudioSegment
        sound = AudioSegment.from_mp3(mp3)
        sound.export(output, format="wav")
        print("done")


def zip(src_dir, dst_dir_name, output):
    import zipfile
    with zipfile.ZipFile(output, 'w') as zf:
        for root, dirs, files in os.walk(src_dir):
            for file in tqdm(files, desc=f"zip {dst_dir_name}"):
                zf.write(os.path.join(root, file),
                         arcname=os.path.join(dst_dir_name, file))
    print(f"zip {dst_dir_name} done. {output}")


current_dir = os.path.dirname(__file__)

mp4_dir = f'{current_dir}/output/mp4'
mp3_dir = f'{current_dir}/output/mp3'
voice_dir = f'{current_dir}/output/voice'
wav_dir = f'{current_dir}/output/wav'
zip_file = f'{current_dir}/output/lain.mp3.zip'

for dir in [mp4_dir, mp3_dir, voice_dir, wav_dir]:
    if not os.path.exists(dir):
        os.makedirs(dir)


def run(name):
    _file = find_ass(name)
    if _file is not None:
        lain_event = get_lain_event(_file)
        mp4 = get_mp4(name, mp4_dir)
        mp3 = get_audio(mp4, mp3_dir)
        for e in lain_event:
            output = f"{voice_dir}/{name}_{e.text}.mp3"
            voice = cut_audio(mp3, e, output)
            # mp3_to_wav(voice, wav_dir)

# 以下のモジュールは十分です
def main():
    # name = "Cou002"
    modules = ["Cou",
               # "Dc",
               # "Dia",
               # "Eda",
               # "Ekm",
               # "Env",
               # "Ere",
               "Lda",
               # "Special",
               # "TaK",
               # "Tda",
               ]
    for module in modules:
        lainass_dir = os.path.join(current_dir, "lainass", module)
        ass_names = []
        for f in os.listdir(lainass_dir):
            pp = os.path.splitext(f)
            if pp[1] == ".ass":
                ass_names.append(pp[0])
        ass_names.sort()
        # ass_names = ass_names[0:5]
        for ass_name in ass_names:
            print(f"run {ass_name}")
            run(ass_name)


init_ass_map()


if __name__ == '__main__':
    main()
    # run("Cou001")
    zip(voice_dir, "lain", zip_file)
