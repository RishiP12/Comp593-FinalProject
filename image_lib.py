import os
import hashlib
import ctypes
import requests
from PIL import Image

def download_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def save_image_file(image_data, image_path):
    try:
        with open(image_path, 'wb') as file:
            file.write(image_data)
        return True
    except IOError as e:
        print(f"Error saving image file: {e}")
        return False

def set_desktop_background_image(image_path):
    if not os.path.isfile(image_path):
        print(f"Error: File not found at {image_path}")
        return False
    
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        return True
    except Exception as e:
        print(f"Failed to set desktop background. Error: {e}")
        return False

def compute_sha256(image_data):
    sha256 = hashlib.sha256()
    sha256.update(image_data)
    return sha256.hexdigest()

if __name__ == '__main__':
    pass
