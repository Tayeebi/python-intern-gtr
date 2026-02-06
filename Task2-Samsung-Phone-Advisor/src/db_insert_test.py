import sys
import requests
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)
    r.raise_for_status()
    return r.text

def get_spec(soup, section, key):

    for table in soup.select("#specs-list table"):
        head = table.select_one("th")
        if not head or head.get_text(strip=True) != section:
            continue

        for row in table.select("tr"):
            k = row.select_one("td.ttl")
            v = row.select_one("td.nfo")
            if k and v and k.get_text(strip=True) == key:
                return v.get_text(" ", strip=True)

    return ""

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php"
soup = BeautifulSoup(get_html(url), "html.parser")

name = soup.select_one("h1.specs-phone-name-title").get_text(strip=True)

release_date = get_spec(soup, "Launch", "Announced")

display_type = get_spec(soup, "Display", "Type")
display_size = get_spec(soup, "Display", "Size")
display = (display_type + " | " + display_size).strip(" |")

battery = get_spec(soup, "Battery", "Type")

camera = ""
for k in ["Quad", "Triple", "Dual", "Single"]:
    camera = get_spec(soup, "Main Camera", k)
    if camera:
        break

memory = get_spec(soup, "Memory", "Internal")   
price = get_spec(soup, "Misc", "Price")

print("name:", name)
print("url:", url)
print("release_date:", release_date)
print("display:", display)
print("battery:", battery)
print("camera:", camera)
print("memory:", memory)
print("price:", price)
