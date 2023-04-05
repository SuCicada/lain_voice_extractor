```bash
pip install ass moviepy wget pydub zipfile
```

mp4 -> mp3 -> voice -> wav


```bash
# Random sampling test voice.
find output/voice -type f -print0 | shuf -n1 -z | xargs -0 sh -c 'echo "$0"; afplay "$0"'

while true; do make voice_sample_test; done


apt install ffmpeg
pip install pydub
python unzip.py lain.mp3.zip so-vits-svc/dataset_raw
```
