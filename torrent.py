import requests
import re


def bluemediafiles_decode_key(encoded):
    key = ''
    half_len = len(encoded) // 2
    for i in range(half_len - 5, -1, -2):
        key += encoded[i]
    for i in range(half_len + 4, len(encoded), 2):
        key += encoded[i]
    return key

# Compile regex patterns once
game_button_pattern = re.compile(r'<a\s+href="(https://gamedownloadurl\.lol/[^"]+)"')
encoded_key_pattern = re.compile(r'Goroi_n_Create_Button\("(?P<encoded>[^"]+)"\);')
magnet_link_pattern = re.compile(r'<a class="button" href="(magnet:[^"]+)"')
file_size_pattern = re.compile(r'<span class="uk-text-meta">Release Size: </span>(\d+(?:(\.|\,)\d+)?(?:\s?(?:MB|GB)))</p>')
datetime_pattern = re.compile(r'<time datetime="([^"]+)"')

def get(session, url):
    
    try:
        response = session.get(url)
        response.raise_for_status()

        game_button = game_button_pattern.search(response.text)
        file_size = file_size_pattern.search(response.text)
        datetime = datetime_pattern.search(response.text)

        if game_button:
            game_url = game_button.group(1)
            response = session.get(game_url)
            response.raise_for_status()

        # Search for the encoded key in the response text
            encoded_key = None
        match = encoded_key_pattern.search(response.text)
        if match:
            encoded_key = match.group('encoded')

        if encoded_key:
            decoded_key = bluemediafiles_decode_key(encoded_key)
            redirect_url = f'https://gamedownloadurl.lol/get-url.php?url={decoded_key}'
            response = session.get(redirect_url)
            response.raise_for_status()
            magnet_link = magnet_link_pattern.search(response.text)
            if magnet_link:
                return magnet_link.group(1), file_size.group(1), datetime.group(1)
                
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    return None