# download files
import requests
from urllib.request import urlretrieve
# files and convert audio
import subprocess
from os import remove
# makes things faster

LINK = 'https://cdnlive2.shooowit.net/rtpalive/smil:radio.smil/'
URL  = f'{LINK}chunklist_b1000000.m3u8'

def log(msg:str):
    print(f'\033[94m{msg}\033[0m')

def fetch_audio(contents:[str]):
    pass


while True:
    contents = [x + (log(f'{x} fetched') or "") for x in requests.get(URL).text.split('\n') if 'media' in x]
    for i, v in enumerate(contents):
        urlretrieve(LINK+v, f'{i}.acc')
        subprocess.run(['ffplay', f'{i}.acc', '-nodisp', '-autoexit', '-v', 'error', '-volume', '30'])
        remove(f'{i}.acc')

