import json

#절대경로 사용할것
with open('경로', 'r', encoding='utf-8') as txt_file:
    lines = txt_file.readlines()

result = []

for line in lines:
    parts = line.strip().split(' ')
    url = parts[0]
    name = ' '.join(parts[1:])
    item = {"url": url, "name": name}
    result.append(item)

with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)


