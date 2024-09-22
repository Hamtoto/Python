import os
import requests
import pandas as pd
from googleapiclient.discovery import build
from PIL import Image
from io import BytesIO
import time

# 엑셀 파일에서 와인 데이터를 읽어오는 함수
def load_wine_data_from_excel(file_path):
    df = pd.read_excel(file_path, header=1)  # 두 번째 행을 컬럼명으로 사용
    print("엑셀 파일에서 읽어온 컬럼명:", df.columns)
    df.columns = df.columns.str.strip()  # 공백 제거
    return df

# 구글 이미지 검색 함수 (검색어에서 특수 문자 제거)
def google_image_search(query, api_key, cse_id, num_images=20):
    # 특수 문자 및 쉼표 제거, 검색어를 간소화
    query = query.replace(',', '').replace('  ', ' ').strip()
    
    service = build("customsearch", "v1", developerKey=api_key)
    try:
        res = service.cse().list(
            q=query,  # 단순화된 검색어 사용
            cx=cse_id,
            searchType="image",
            num=num_images,  # 검색 결과 수를 10개로 감소
            imgSize="LARGE",
            imgType="photo",
            safe="active"
        ).execute()

        if 'items' in res:
            image_links = [item['link'] for item in res['items']]
            return image_links
        else:
            print(f"No results found for query: {query}")
            return []
    except Exception as e:
        print(f"Error occurred during image search: {str(e)}")
        return []

# 이미지 다운로드 함수 (압축 없이 바로 저장)
def download_images(image_urls, wine_name, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    bottle_images_dir = os.path.join(save_dir, "bottle_images")
    if not os.path.exists(bottle_images_dir):
        os.makedirs(bottle_images_dir)

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            # 이미지 파일 저장
            final_path = os.path.join(bottle_images_dir, f"{wine_name}_{idx + 1}.jpg")
            img.save(final_path, format="JPEG")
            print(f"Saved image for {wine_name} at {final_path}")
        except Exception as e:
            print(f"Error processing image {idx + 1} for {wine_name}: {str(e)}")

# 메인 함수 (검색어 단순화 및 특수 문자 제거)
def main(excel_file, google_api_key, cse_id, save_dir="wine_images"):
    wines = load_wine_data_from_excel(excel_file)

    for idx, row in wines.iterrows():
        wine_name = row['상품명']  # B3 열의 와인명 사용
        
        # 검색어 단순화 (특수 문자 제거)
        query = f"{wine_name}"
        print(f"Searching images for: {query}")

        image_urls = google_image_search(query, google_api_key, cse_id)
        
        if image_urls:
            download_images(image_urls, wine_name, save_dir)
        else:
            print(f"No images found for: {wine_name}")
        
        # API 호출 간 딜레이 추가 (rate limit 방지)
        time.sleep(10)  # 10초 간 딜레이

# 실행 예시
if __name__ == "__main__":
    google_api_key = ""
    cse_id = ""
    excel_file = "Wine_crawling/wine_2024091302.xlsx"  # 엑셀 파일 경로

    main(excel_file, google_api_key, cse_id)

