import os
import sys
import requests
import ctypes
from datetime import datetime
import hashlib
import sqlite3

def validate_date(date_str):
    """Validate the provided date string."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date > datetime.now():
            raise ValueError("APOD date cannot be in the future")
        return date.strftime("%Y-%m-%d")
    except ValueError as e:
        if "does not match format" in str(e):
            print(f"Error: Invalid date format; time data '{date_str}' does not match format '%Y-%m-%d'")
        else:
            print(f"Error: Invalid date format; {e}")
        print("Script execution aborted.")
        sys.exit(1)

def get_apod_info(date_str, api_key):
    """Fetch APOD information for a given date from the NASA API."""
    url = f"https://api.nasa.gov/planetary/apod?date={date_str}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching APOD info: {response.text}")
    return response.json()

def download_image(image_url, save_path):
    """Download image from the given URL and save it to the specified path."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception("Failed to download image")

def calculate_sha256(file_path):
    """Calculate the SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def initialize_cache_db(db_path):
    """Initialize the image cache database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS apod_cache 
                      (title TEXT, date TEXT, file_path TEXT, sha256 TEXT)''')
    conn.commit()
    return conn

def add_to_cache_db(conn, title, date, file_path, sha256):
    """Add an APOD entry to the cache database."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO apod_cache (title, date, file_path, sha256) VALUES (?, ?, ?, ?)", 
                   (title, date, file_path, sha256))
    conn.commit()

def set_desktop_background_image(image_path):
    """Set the desktop background to the specified image."""
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    except Exception as e:
        print(f"Failed to set desktop background. Error: {e}")
        print("Failed to set APOD image as desktop background.")
        sys.exit(1)

def main(apod_date_str):
    # Step 1: Validate and parse the date
    apod_date = validate_date(apod_date_str)
    print(f"APOD date: {apod_date}")

    # Step 2: Initialize directories and database
    image_cache_dir = os.path.join("C:\\FinalProject\\images")
    os.makedirs(image_cache_dir, exist_ok=True)
    print(f"Image cache directory: {image_cache_dir}")

    db_path = os.path.join(image_cache_dir, "image_cache.db")
    db_created = not os.path.exists(db_path)
    conn = initialize_cache_db(db_path)
    if db_created:
        print(f"Image cache DB created: {db_path}")
    else:
        print(f"Image cache DB: {db_path}")

    # Step 3: Get APOD info from NASA
    api_key = "DEMO_KEY"  
    try:
        print(f"Getting {apod_date} APOD information from NASA...", end="")
        apod_info = get_apod_info(apod_date, api_key)
        print("success")
    except Exception as e:
        print(e)
        print("Script execution aborted.")
        sys.exit(1)

    apod_title = apod_info['title']
    apod_url = apod_info['url']
    print(f"APOD title: {apod_title}")
    print(f"APOD URL: {apod_url}")

    # Step 4: Download APOD image
    image_filename = apod_title.replace(" ", "_").replace(":", "") + ".jpg"
    image_path = os.path.join(image_cache_dir, image_filename)
    try:
        print(f"Downloading image from\n{apod_url}...", end="")
        download_image(apod_url, image_path)
        print("success")
    except Exception as e:
        print(f"Error downloading image: {e}")
        print("Script execution aborted.")
        sys.exit(1)

    # Step 5: Check if the image is already in cache
    apod_sha256 = calculate_sha256(image_path)
    print(f"APOD SHA-256: {apod_sha256}")

    # Step 6: Save the image info to the cache DB
    print(f"Adding APOD to image cache DB...", end="")
    add_to_cache_db(conn, apod_title, apod_date, image_path, apod_sha256)
    print("success")

    # Step 7: Set the desktop background
    print(f"Setting desktop to {image_path}...", end="")
    set_desktop_background_image(image_path)
    print("success")

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python apod_desktop.py <YYYY-MM-DD>")
        sys.exit(1)

    main(sys.argv[1])
