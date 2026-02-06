import requests
from bs4 import BeautifulSoup

list_url = "https://www.gsmarena.com/samsung-phones-9.php"
base = "https://www.gsmarena.com/"

html = requests.get(list_url, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

# phone cards on this page
a_tags = soup.select("div.makers ul li a")

# print first 10 phone links
for a in a_tags[:50]:
    print(base + a["href"])
