import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def get_cal_fatsecret(food):
    url = f"https://www.fatsecret.co.in/calories-nutrition/search?q={urllib.parse.quote(food)}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # find the prominent tag
        prominent = soup.find(class_='prominent')
        if prominent:
            match = re.search(r'(\d+)\s*kcal', prominent.text)
            if match:
                return int(match.group(1))
    except:
        pass
    return None

print('aloo gobi:', get_cal_fatsecret('aloo gobi'))
