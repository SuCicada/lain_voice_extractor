from pydub import AudioSegment
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# 设置MP3文件所在的文件夹路径
mp3_folder = "output/voice"

# 定义线程池
executor = ThreadPoolExecutor(max_workers=8)

# 定义计算总时长的函数
def calculate_duration(mp3_file):
    audio = AudioSegment.from_file(mp3_file, format="mp3")
    return len(audio)

# 遍历文件夹中的所有MP3文件，计算总时长
total_duration = 0
futures = []
for filename in os.listdir(mp3_folder):
    if filename.endswith(".mp3"):
        mp3_file = os.path.join(mp3_folder, filename)
        future = executor.submit(calculate_duration, mp3_file)
        futures.append(future)

# 等待所有计算完成，并将结果相加
for future in tqdm(as_completed(futures), total=len(futures)):
    total_duration += future.result()

# 输出总时长
total_seconds = total_duration / 1000
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
print(f"Total duration: {hours:.0f}h {minutes:.0f}m {seconds:.0f}s")
