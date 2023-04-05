import json

data_json = "data.json"
res = ""
with open(data_json, "r") as f:
    data = json.load(f)
for k,v in data.items():
    res += f"dataset/{k}.wav|{v}\n"

with open("data.txt", "w") as f:
    f.write(res)
