import openai
import pandas as pd
import json
import os

# GPT API 키 설정
openai.api_key = ""

def get_original_wine_name(plu_nm):
    # GPT-4에 전송할 프롬프트 작성
    messages = [
        {"role": "system", "content": "당신은 술 전문가 입니다. 사용자가 한국에서 유통되는 와인 이름을 말할건데 해당 와인의 원래 이름을 찾아서 Json 형식으로 응답합니다."},
        {"role": "user", "content": f"와인 이름: {plu_nm}"}
    ]
    
    # GPT-4 API 호출
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=100,
        temperature=0.2,
        top_p=0.5,
    )
    
    # 응답에서 JSON 추출
    try:
        response_text = response['choices'][0]['message']['content'].strip()
        wine_info = json.loads(response_text)
        return wine_info
    except (json.JSONDecodeError, IndexError, KeyError):
        return {"name_original": None, "name_kr": plu_nm}

def process_csv(input_csv_path, output_json_path):
    # CSV 파일 불러오기
    df = pd.read_csv(input_csv_path, sep='|')
    
    # 원래 와인 이름 찾기 및 JSON 데이터 생성
    results = []
    for idx, row in df.iterrows():
        print(f"Processing row {idx+1}: {row.to_dict()}")
        wine_info = get_original_wine_name(row['PLU_NM'])
        print(f"Wine info: {wine_info}")
        result = {
            "STORE_CD": row['STORE_CD'],
            "PLU_CD": row['GPLU_CDNRL_PRC'],
            "SCAN_CD1": row['SCAN_CD1'],
            "SCAN_CD2": row['SCAN_CD2'],
            "PLU_NM": row['PLU_NM'],
            "name_original": wine_info.get("name_original"),
            "name_kr": wine_info.get("name_kr"),
            "BRAND_CD": row['BRAND_CD'],
            "GPLU_CDNRL_PRC": row['GPLU_CDNRL_PRC'],
            "PRC_EVT_PRC": row['PRC_EVT_PRC'],
            "PRC_EVT_ST_DT": row['PRC_EVT_ST_DT'],
            "PRC_EVT_ED_DT": row['PRC_EVT_ED_DT']
        }
        results.append(result)
        print(f"Result appended: {result}")
    
    # 결과를 JSON 파일로 저장
    try:
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)
    except (OSError, IOError) as e:
        print(f"Error writing to file {output_json_path}: {e}")

if __name__ == "__main__":
    input_csv_path = "C:/Users/PC/PycharmProjects/Python/Wine_crawling/wine_data.csv"  # 입력 CSV 파일 경로
    output_json_path = "./output.json"  # 출력 JSON 파일 경로
    process_csv(input_csv_path, output_json_path)
    print(f"Processed data saved to {output_json_path}")
