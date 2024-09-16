from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, pipeline
from PIL import Image
import torch
import urllib3
import requests
import os
from moviepy.editor import VideoFileClip, ImageClip
import json
import csv
from Data import unsplash_access_key, pexel_api_key

caption = False

if caption:
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

def generate_caption(image_path):

    # Load and preprocess the image
    image = Image.open(image_path)
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values

    # Generate the caption
    with torch.no_grad():
        output_ids = model.generate(pixel_values, max_length=16, num_beams=4, return_dict_in_generate=True).sequences
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return caption

def item_is_folder(path):
    if os.path.isdir(path):
        return True
    return False

def fetch_unsplash_images(query, access_key=unsplash_access_key, page=1, per_page=30):
    url = 'https://api.unsplash.com/search/photos'
    headers = {
        'Authorization': f'Client-ID {access_key}'  # Use only the Access Key here
    }
    params = {
        'query': query,
        'per_page': per_page,
        'page': page
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        results = response.json()
        return results['results']
    else:
        print(f"Error: {response.status_code}")
        return None

def get_caption_by_url(image):
    return generate_caption(f"/content/drive/MyDrive/SocialMediaAI/Videos/Images/{image}.jpg")


def saveImg(url, save_as):
      http = urllib3.PoolManager()
      response = http.request('GET', url)
      with open(save_as, 'wb') as file:
          file.write(response.data)
      return True

def delete_files():
    for i in os.listdir("D:/ICTsocials/Videos/Images"):
        if i == "Json":
            for j in os.listdir(os.path.join("D:/ICTsocials/Videos/Images", "Json")):
                os.remove(os.path.join("D:/ICTsocials/Videos/Images", "Json", j))
        else:
            if item_is_folder(os.path.join("D:/ICTsocials/Videos/Images", i)):
                for k in os.listdir(os.path.join("D:/ICTsocials/Videos/Images", i)):
                    os.remove(os.path.join("D:/ICTsocials/Videos/Images", i, k))
                os.rmdir(os.path.join("D:/ICTsocials/Videos/Images", i))
            else:
                os.remove(os.path.join("D:/ICTsocials/Videos/Images", i))


def getImages(query, page=1, per_page=30, query_video=None, img_get=30, max_videos=30, save_directory="Videos/Images/",
              api_key=pexel_api_key, download_videos=True):

    delete_files()

    images = 0
    response_obj = []
    json_obj = {}

    # Reading the IDs to delete
    with open("Videos/delete.csv", "r") as file:
        reader = csv.reader(file)
        ids_del = set()
        for row in reader:
            ids_del.update(row)

    if download_videos:
        query_video = query if query_video is None else query_video
        download_videos_from_pexels(query_video, save_directory, api_key, per_page=10, max_videos=max_videos)

    while images < img_get:
        response = fetch_unsplash_images(query, page=page, per_page=per_page)
        if not response:  # Break the loop if no images are returned
            break

        for index, i in enumerate(response):
            id = i["id"]
            if id in ids_del:
                continue

            desc = i["description"]
            width = i["width"]
            height = i["height"]
            url = i["urls"]["full"]
            path = f"{save_directory}Image_{images}.jpg"  # Save as per current image count
            response = saveImg(url=url, save_as=path)

            if not response:
                return None

            obj = {
                "desc": desc if desc else generate_caption(path) if caption else None,
                "width": width,
                "height": height,
                "url": url,
                "name": path,
                "index": images,  # Use the image count as index
                "id": id
            }
            json_obj[f"Image_{images}"] = obj
            response_obj.append(obj)
            crop_to_aspect_ratio(path, path)
            images += 1

        page += 1

    with open(f"Videos/Data.json", "w") as file:
        json.dump(json_obj, file, indent=2)

    for key, data in json_obj.items():
        with open("Videos/Images/Json/"+key+'.json', 'w') as file:
            json.dump(data, file, indent=2)

    return response_obj  # Optionally return the response object

def crop_to_aspect_ratio(image_path, output_path):
    # Open the image
    with Image.open(image_path) as img:
        # Get current image dimensions
        width, height = img.size

        # Define the target aspect ratio and dimensions
        target_aspect_ratio = (9, 16)
        target_width = width
        target_height = int(width * target_aspect_ratio[1] / target_aspect_ratio[0])

        if target_height > height:
            target_height = height
            target_width = int(height * target_aspect_ratio[0] / target_aspect_ratio[1])

        # Calculate the cropping box
        left = (width - target_width) / 2
        top = (height - target_height) / 2
        right = (width + target_width) / 2
        bottom = (height + target_height) / 2

        # Crop the image to the desired aspect ratio
        img_cropped = img.crop((left, top, right, bottom))

        # Resize the cropped image to 1080x1920
        img_resized = img_cropped.resize((1080, 1920), Image.LANCZOS)

        # Save the final image
        img_resized.save(output_path)

motivation_keywords = ["motivation", "hard work", "work", "discipline", "persistence", "success", "growth", "achievement", "inspirational", "trading"]
cryptocurrency_news_keyswords = ["cryptocurrency", "trading", "blockchain", "bitcoin", "ethereum", "AI", "future", "science"]


def create_zoom_effect(image_path, zoom_factor=1.2, duration=2):
    clip = ImageClip(image_path).set_duration(duration)
    clip = clip.resize(lambda t: 1 + (zoom_factor - 1) * (t / duration))
    return clip

def resize_image(input_path, output_path):
    # Load the image
    img = Image.open(input_path)
    original_width, original_height = img.size

    # Target dimensions
    target_width = 1024
    target_height = 576

    # Calculate the aspect ratios
    target_ratio = target_width / target_height
    current_ratio = original_width / original_height

    if current_ratio < 1:  # Portrait or square
        # Calculate new width to match the target aspect ratio
        new_width = int(original_height * target_ratio)
        extend_width = new_width - original_width

        # Create a new image with the extended width
        new_img = Image.new('RGB', (new_width, original_height))

        # Extend the borders using the last 3 pixels on the left and right sides
        left_border = img.crop((0, 0, 3, original_height))
        right_border = img.crop((original_width - 3, 0, original_width, original_height))

        # Paste the borders
        for x in range(0, extend_width // 2):
            new_img.paste(left_border, (x, 0))
        new_img.paste(img, (extend_width // 2, 0))
        for x in range(new_width - (extend_width // 2), new_width):
            new_img.paste(right_border, (x, 0))

        # Resize the image to the target dimensions
        img = new_img.resize((target_width, target_height))

    else:  # Landscape
        # Calculate the new dimensions to crop and resize
        new_width = min(original_width, int(original_height * target_ratio))
        left = (original_width - new_width) // 2
        right = left + new_width

        img = img.crop((left, 0, right, original_height))
        img = img.resize((target_width, target_height))

    # Save the resulting image
    img.save(output_path)

def download_videos_from_pexels(query, save_directory, api_key, per_page=10, max_videos=50, page_begin=1):
    """
    Downloads videos from Pexels based on a query and saves them to a specified directory.

    Args:
    - query (str): The search query to find videos on Pexels.
    - save_directory (str): The directory where the videos should be saved.
    - api_key (str): Your Pexels API key.
    - per_page (int): The number of videos to retrieve per page (default is 10).
    - max_videos (int): The maximum number of videos to download (default is 50).
    - page_begin (int): The starting page number for the search (default is 1).

    Returns:
    - str: A message indicating the result of the operation.
    """
    try:
        with open("Videos/delete.csv", "r") as file:
            reader = csv.reader(file)
            ids_del = set()
            for row in reader:
                ids_del.update(row)
        # Ensure the save directory exists
        os.makedirs(save_directory, exist_ok=True)

        # Set up the initial parameters for the search
        url = "https://api.pexels.com/videos/search"
        headers = {
            "Authorization": api_key
        }
        params = {
            "query": query,
            "per_page": per_page,
            "page": page_begin
        }

        downloaded_videos = 0

        while downloaded_videos < max_videos:
            # Make the request to search for videos
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Check if the request was successful
            video_data = response.json()

            # If no videos are found, break the loop
            if not video_data['videos']:
                break

            # Download each video
            for video in video_data['videos']:
                if downloaded_videos >= max_videos:
                    break

                video_id = video['id']
                if video_id in ids_del:
                    continue
                video_url = video['video_files'][0]['link']
                video_format = video['video_files'][0]['file_type']
                image_url = video['video_pictures'][0]['picture']

                # Create a directory for each video using its ID
                video_directory = os.path.join(save_directory, str(video_id))
                os.makedirs(video_directory, exist_ok=True)  # Ensure the directory exists

                save_path = os.path.join(video_directory, "Video.mp4")
                save_img_path = os.path.join(video_directory, "Image.png")

                # Download the video content
                video_response = requests.get(video_url)
                video_response.raise_for_status()

                # Save the video to the specified path
                with open(save_path, "wb") as video_file:
                    video_file.write(video_response.content)

                # Download and save the image
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                if caption:
                    caption2 = generate_caption(save_img_path)
                    with open(os.path.join(video_directory, 'caption.json'), 'w') as file:
                        file.write(caption2)

                with open(save_img_path, "wb") as image_file:
                    image_file.write(image_response.content)

                crop_to_9_16(save_path)

                downloaded_videos += 1
                print(f"Downloaded video {downloaded_videos}/{max_videos}: {save_path}")

            # Move to the next page
            params['page'] += 1

        return f"Downloaded {downloaded_videos} videos to {save_directory}", params['page']

    except Exception as e:
        raise e

def crop_to_9_16(video_path, output_path=None):
    # Load the video
    video = VideoFileClip(video_path)

    # Calculate the original dimensions
    width, height = video.size

    # Calculate the target dimensions
    target_height = height
    target_width = int(target_height * 9 / 16)

    if target_width > width:
        # If the target width is greater than the original width, adjust accordingly
        target_width = width
        target_height = int(target_width * 16 / 9)

    # Calculate cropping margins
    left_margin = (width - target_width) / 2
    right_margin = left_margin + target_width
    top_margin = (height - target_height) / 2
    bottom_margin = top_margin + target_height

    # Crop the video to the desired aspect ratio
    cropped_video = video.crop(x1=left_margin, x2=right_margin, y1=top_margin, y2=bottom_margin)

    resized_video = cropped_video.resize(newsize=(1080, 1920))

    # Determine output path
    if output_path is None:
        output_path = video_path

    # Write the cropped video to the output path
    resized_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

if __name__ == '__main__':
    getImages("cryptocurrency", download_videos=False)
