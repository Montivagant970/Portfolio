"""The following code automatically scrapes audio content from a webpage where the audio data is embedded. This code will need to be altered for the specific needs of each website's HTML structure.

This tool was developed for my master's thesis on "Automatic Speech Recognition for the South Tyrolean German Dialects"."""
import requests
from bs4 import BeautifulSoup
import re
import os

os.chdir('/path/to/desired/working/directory')

## Step-One : Create dictionary of episode links
url = 'https://www.podcast.de/podcast/website/link'

r = requests.get(url)
source = r.text
soup = BeautifulSoup(source)

episodes = {}
pages = {}

for element in soup.find_all('a'):
  elementtext = element.get_text()
  # print(elementtext)
  if re.match('(\d+|\W+\d+|\n)', elementtext) != None:
    link = element['href']
    # print(link)

    if re.match('\d+', elementtext) != None:
      pages[elementtext] = link
    else:
      episodes[elementtext] = link

for page in pages:
  url = pages[page]

  r = requests.get(url)
  source = r.text
  soup = BeautifulSoup(source)

  for element in soup.find_all('a'):
    elementtext = element.get_text()
    if re.match('(\d+|\W+\d+|\n)', elementtext) != None:
      link = element['href']

      if re.match('\d+', elementtext) != None:
        pass
      else:
        episodes[elementtext] = link

## Step-Two : Scrape download links
downloadlinks = {}
for title, hyper in episodes.items():
  newtitle = title[54:]
  r = requests.get(hyper)
  source = r.text
  soup = BeautifulSoup(source)

  for element in soup.find_all('a'):
    if 'podcast' in element['href']:
      elementtext = element.get_text()
      link = element['href']

      if 'anchor' in link:
        downloadlinks[newtitle] = link

## Step-Three: Download audios
for title, link in downloadlinks.items():
  newtitle = re.findall('\d+', title)

  audio = requests.get(link)
  # info = mediainfo(audio.content)
  # print(info.get('format_name', None))

  with open (f'PodcastName_{newtitle[0]}.mp3', 'wb') as f: #CHANGE NAME FOR EACH PODCAST
    print(f'Downloading audio {newtitle[0]}.')
    f.write(audio.content)
