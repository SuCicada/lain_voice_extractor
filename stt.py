# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import json
import os
import threading
import time

import openai
from dotenv import load_dotenv
load_dotenv()  # load variables from .env file

openai.api_key =  os.getenv("OPENAI_API_KEY")


def stt(filename):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # print(transcript["text"])
    return transcript["text"]
    # time.sleep(0.3)
    # return "あdfあsd"


import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

data_json = "data.json"
if not os.path.exists(data_json):
    data = {}
    with open(data_json, "w") as f:
        json.dump(data, f)

# 定义线程池
executor = ThreadPoolExecutor(max_workers=10)
lock = threading.Lock()


# 定义获取文件名的函数
def get_file_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]

with open(data_json, "r") as f:
    data = json.load(f)

# 定义处理单个文件的函数
def process_file(filename):
    # 读取JSON文件
    name = get_file_name(filename)
    # 判断是否已经存在于JSON中
    if name in data:
        return
    # 运行函数获取值
    value = stt(filename)
    print(f"{name}: {value}")
    # 更新JSON
    with lock:
        data[name] = value
        # print(data)
        with open(data_json, "w") as f:
            json.dump(data, f,ensure_ascii=False)


# 遍历目录中的所有MP3文件，并使用并发方式处理
mp3_folder = "output/voice"
futures = []
filenames = sorted([f for f in os.listdir(mp3_folder)])
for filename in filenames:
    if filename.endswith(".mp3"):
        mp3_file = os.path.join(mp3_folder, filename)
        future = executor.submit(process_file, mp3_file)
        futures.append(future)

# 等待所有计算完成
for future in tqdm(as_completed(futures), total=len(futures)):
    future.result()


with open(data_json, "r") as f:
    data = json.load(f)
    print(len(data))
