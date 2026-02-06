import random
import time
import re
import sys
import requests
from bs4 import BeautifulSoup
import psycopg2

BASE = "https://www.gsmarena.com/"

MAX_PAGES = 29      
MAX_ITEMS = 30     
SKIP_TAB_WATCH = True

LIST_DELAY = (2.0, 4.0)    
PHONE_DELAY = (2.5, 5.0)  

MAX_429_TRIES = 6
MAX_429_WAIT = 20         

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
})

def sleep_rand(a, b):
    time.sleep(random.uniform(a, b))

def get_html(url):
    """
    Download HTML.
    If 429 happens, wait a small amount and retry.
    If still blocked after some tries, stop with a clear message.
    """
    for attempt in range(1, MAX_429_TRIES + 1):
        r = session.get(url, timeout=25)

        if r.status_code == 429:

            wait = min(MAX_429_WAIT, 2 * attempt + random.random() * 2)
            print(f"429 blocked -> wait {wait:.1f}s -> retry {attempt}/{MAX_429_TRIES}: {url}")
            time.sleep(wait)
            continue

        r.raise_for_status()
        return r.text

    raise RuntimeError("Still blocked (429). Switch hotspot / wait a bit, then rerun.")

def page_url(page):
    if page == 1:
        return "https://www.gsmarena.com/samsung-phones-9.php"
    return f"https://www.gsmarena.com/samsung-phones-f-9-0-p{page}.php"

def get_phone_links():
    links = []
    seen = set()

    for page in range(1, MAX_PAGES + 1):
        url = page_url(page)
        print(f"Reading list page {page}: {url}")

        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.select("div.makers ul li a")

        if not tags:
            print("No items found on this page. Stop.")
            break

        for a in tags:
            href = a.get("href", "")
            if not href:
                continue

            if SKIP_TAB_WATCH and ("galaxy_tab" in href or "watch" in href):
                continue

            full = BASE + href
            if full in seen:
                continue

            seen.add(full)
            links.append(full)

            if len(links) >= MAX_ITEMS:
                return links

        sleep_rand(*LIST_DELAY)

    return links

def get_spec(soup, section, key):
    for table in soup.select("#specs-list table"):
        th = table.select_one("th")
        if not th or th.get_text(strip=True) != section:
            continue

        for row in table.select("tr"):
            k = row.select_one("td.ttl")
            v = row.select_one("td.nfo")
            if k and v and k.get_text(strip=True) == key:
                return v.get_text(" ", strip=True)

    return ""

def split_memory(text):
    t = text or ""

    ram_match = re.search(r"(\d+)\s*GB\s*RAM", t)
    ram = (ram_match.group(1) + "GB") if ram_match else ""

    tb_match = re.search(r"(\d+)\s*TB", t)
    if tb_match:
        storage = tb_match.group(1) + "TB"
    else:
        gb_match = re.search(r"(\d+)\s*GB(?!\s*RAM)", t)
        storage = (gb_match.group(1) + "GB") if gb_match else ""

    return ram, storage

def scrape_one(phone_url):
    html = get_html(phone_url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one("h1.specs-phone-name-title")
    if not title:
        return None

    name = title.get_text(strip=True)

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
    ram, storage = split_memory(memory)

    price = get_spec(soup, "Misc", "Price")

    return (name, phone_url, release_date, display, battery, camera, ram, storage, price)

def main():
    try:
        links = get_phone_links()
        print("Links found:", len(links))

        if not links:
            print("No links found. Stop.")
            return

        db = psycopg2.connect("dbname=samsung_db user=tayeebi")
        cur = db.cursor()

        saved = 0

        for i, url in enumerate(links, start=1):
            print(f"\n[{i}/{len(links)}] Scraping: {url}")

            try:
                info = scrape_one(url)
                if not info:
                    print("Skipped (no title).")
                    continue

                cur.execute(
                    """
                    INSERT INTO phones
                    (model_name, url, release_date, display, battery, camera, ram, storage, price, scraped_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())
                    ON CONFLICT (url) DO NOTHING;
                    """,
                    info
                )
                db.commit()

                if cur.rowcount == 1:
                    saved += 1
                    print("Saved ✅:", info[0])
                else:
                    print("Already exists:", info[0])

                sleep_rand(*PHONE_DELAY)

            except Exception as e:
                db.rollback()
                print("Error on this phone:", e)

        cur.close()
        db.close()

        print("\nDone ✅ New saved:", saved)

    except Exception as e:
        print("\nStopped:", e)
        print("Tip: turn on hotspot, wait 2–5 minutes, then rerun.")
        sys.exit(1)

if __name__ == "__main__":
    main()
