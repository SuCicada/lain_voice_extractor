import sys
import os
from zipfile import ZipFile
from pydub import AudioSegment
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# read zip file name from command line arguments
zip_file = sys.argv[1]
dir_path = sys.argv[2]

# unzip file to current directory
with ZipFile(zip_file, 'r') as zip:
    zip.extractall(dir_path)
lain_dir = os.path.join(dir_path, "lain")

# loop through all mp3 files in lain directory

mp3_files = [os.path.join(lain_dir, file)
             for file in os.listdir(lain_dir)
             if file.endswith('.mp3')]


def convert_mp3(mp3_file):
    try:
        # load mp3 file
        sound = AudioSegment.from_mp3(mp3_file)
        # create new wav file name
        wav_file = os.path.join(lain_dir, os.path.splitext(os.path.basename(mp3_file))[0] + '.wav')
        # export wav file
        sound.export(wav_file, format="wav")
        # delete original mp3 file
        os.remove(mp3_file)
    except Exception as e:
        print(f"Error converting {mp3_file}: {e}")
        raise e


def check():
    files = [file for file in os.listdir(lain_dir)]
    assert len(files) == len(mp3_files), \
        f"{len(files)} !== {len(mp3_files)}"
    for file in files:
        assert file.endswith('.wav'), \
            f"{file} does not have the suffix .wav"


def run():
    with ThreadPoolExecutor(max_workers=5) as executor:
        # submit each MP3 file's conversion to the thread pool
        futures = [executor.submit(convert_mp3, mp3_file)
                   for mp3_file in mp3_files]
        for future in tqdm(as_completed(futures), total=len(futures)):
            # check if any exception was raised during the conversion
            future.result()


run()
check()
