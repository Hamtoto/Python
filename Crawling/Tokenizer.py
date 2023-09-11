import json

with open('C:\\Users\gohg0\OneDrive\Documents\works\새 폴더\python\Crawling\data.txt', 'r', encoding='utf-8') as txt_file:
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
