import requests, re
from bs4 import BeautifulSoup
import json
import torrent

url = 'https://pcgamestorrents.com/games-list-pc-616134483-torrent-download-free.html'  # Replace with the actual URL

# Send a GET request to the site
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <a> elements within <li> that have rel="noopener noreferrer"
    links = soup.select('li > a[rel="noopener noreferrer"]')
    
    link_data = []
    session = requests.Session()

    for i, link in enumerate(links[:5]):
        #start = time.time()
        #print(f"{i + 1}/{len(links)} | ETA: {(length * (len(links) - 1))/60.0:.2f}m")
        
        magnet, size, date = torrent.get(session, link.get('href'))
        
        link_info = {
            'title': link.get_text(strip=True),
            'uris': [magnet],
            'uploadDate': date,
            'fileSize': size
        }

        link_data.append(link_info)
    
    export = {
        'name': 'IGGGames',
        'downloads': link_data
    }
    
    # Convert the list of dictionaries to JSON with actual symbols
    json_data = json.dumps(export, ensure_ascii=False, indent=4)
    
    # Write the JSON data to a file with UTF-8 encoding
    with open('links.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)
    
    print("Data has been written to links.json")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
