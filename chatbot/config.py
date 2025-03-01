import os

def get_api_key():

    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("API Key not found. Please set GOOGLE_API_KEY environment variable.")
    return api_key
