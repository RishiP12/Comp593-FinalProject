import requests

def get_apod_info(apod_date, api_key):
    """Gets information from the NASA API for the Astronomy Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (str): APOD date (formatted as YYYY-MM-DD)
        api_key (str): Your NASA API key

    Returns:
        dict: Dictionary of APOD info if successful, None if unsuccessful
    """
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "date": apod_date,
        "thumbs": True  # Get video thumbnail if APOD is a video
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response as a dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching APOD info: {e}")
        return None

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high-definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from the API

    Returns:
        str: APOD image URL if found, None otherwise
    """
    if not apod_info_dict:
        return None

    if apod_info_dict.get('media_type') == 'image':
        return apod_info_dict.get('hdurl') or apod_info_dict.get('url')
    elif apod_info_dict.get('media_type') == 'video':
        return apod_info_dict.get('thumbnail_url')
    return None
