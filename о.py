from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re


def know_text_in_link(link):
    resp = requests.get(link)
    if 300 > resp.status_code >= 200:
        html = urlopen(link).read()
        soup = BeautifulSoup(html, features="html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    return f'Ошибка программы {resp.status_code}'


url = "https://drive.google.com/drive/folders/1z-cmYoHxQqZbVZMXg73ucQWTedQZM8o4"
print(know_text_in_link(url))