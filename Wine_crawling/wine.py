import os
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from PIL import Image
from io import BytesIO


#open file
def load_wine_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        wines = [line.strip() for line in file.readlines()]
    return wines


#google image search
def google_image_search(query, api_key, cse_id, num_images=4):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(
        q=query,
        cx=cse_id,
        searchType="image",
        num=num_images,
        imgSize="LARGE"
    ).execute()
    image_links = [item['link'] for item in res['items']]
    return image_links




#Download and save images
def download_images(image_urls, wine_name, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for idx, url in enumerate(image_urls):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # PNG로 변환하여 저장
        img = img.convert("RGBA")  #png로 변환
        img.save(os.path.join(save_dir, f"{wine_name}_{idx + 1}.png"), format="PNG")


#main
def main(wine_file, api_key, cse_id, save_dir="wine_images"):
    wines = load_wine_names(wine_file)

    for wine in wines:
        print(f"Searching images for {wine}")
        image_urls = google_image_search(wine, api_key, cse_id)
        download_images(image_urls, wine, save_dir)
        print(f"Saved images for {wine}")


if __name__ == "__main__":
    #API, Search ID
    api_key = ""
    cse_id = ""

    #file path
    wine_file = "./name.txt"

    #start
    main(wine_file, api_key, cse_id)
