import os
import requests
import json

with open('C:/Users/Admin/Documents/work/python/Crawling/data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

for item in data:
    url = item['url']
    name = item['name']

    response = requests.get(url)
    
    if response.status_code == 200:
        file_path = os.path.join(os.getcwd(), name)
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f'{name} 다운로드 및 저장 완료.')
    else:
        print(f'{name} 다운로드 실패. 상태 코드: {response.status_code}')
