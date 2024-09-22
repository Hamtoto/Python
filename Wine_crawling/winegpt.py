import os
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from PIL import Image
from io import BytesIO
import base64


def load_wine_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        wines = [line.strip() for line in file.readlines()]
    return wines


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


def compress_image(image, max_size=(800, 800), quality=85):
    img = image.copy()
    img.thumbnail(max_size)

    # Convert to RGB if the image has an alpha channel
    if img.mode in ('RGBA', 'LA'):
        background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
        background.paste(img, img.split()[-1])
        img = background

    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=quality, optimize=True)
    return Image.open(buffered)


def check_wine_bottle_image(image_path, perplexity_api_key):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are an AI assistant that analyzes images."},
            {"role": "user",
             "content": f"Is this image a full wine bottle? Respond with only 'Yes' or 'No'. Image: data:image/jpeg;base64,{encoded_image}"}
        ]
    }

    response = requests.post("https://api.perplexity.ai/chat/completions", json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip().lower() == 'yes'
    else:
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        return False


def download_and_check_images(image_urls, wine_name, save_dir, perplexity_api_key):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    bottle_images_dir = os.path.join(save_dir, "bottle_images")
    if not os.path.exists(bottle_images_dir):
        os.makedirs(bottle_images_dir)

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            # Compress the image
            compressed_img = compress_image(img)

            temp_path = os.path.join(save_dir, f"{wine_name}_{idx + 1}_temp.jpg")
            compressed_img.save(temp_path, format="JPEG")

            if check_wine_bottle_image(temp_path, perplexity_api_key):
                final_path = os.path.join(bottle_images_dir, f"{wine_name}_{idx + 1}.jpg")
                os.rename(temp_path, final_path)
                print(f"Saved compressed bottle image for {wine_name}")
            else:
                os.remove(temp_path)
                print(f"Removed non-bottle image for {wine_name}")
        except Exception as e:
            print(f"Error processing image {idx + 1} for {wine_name}: {str(e)}")


def main(wine_file, google_api_key, cse_id, perplexity_api_key, save_dir="wine_images"):
    wines = load_wine_names(wine_file)

    for wine in wines:
        print(f"Searching images for {wine}")
        image_urls = google_image_search(wine, google_api_key, cse_id)
        download_and_check_images(image_urls, wine, save_dir, perplexity_api_key)


if __name__ == "__main__":
    google_api_key = ""
    cse_id = ""
    perplexity_api_key = ""
    wine_file = "./name.txt"

    main(wine_file, google_api_key, cse_id, perplexity_api_key)