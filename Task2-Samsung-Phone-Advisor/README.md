# ✅ Samsung Phone Advisor (GSMArena → PostgreSQL → FastAPI)

This project **scrapes Samsung phone specs from GSMArena**, saves them into **PostgreSQL**, and runs a **FastAPI** service so you can ask questions like **phone comparisons**.

---

## ✅ Features

- ✅ Scrape Samsung phone list pages (multi-page)
- ✅ Visit each phone page and collect specs:
  - Model Name, URL, Release Date, Display, Battery, Camera, RAM, Storage, Price
- ✅ Store everything in PostgreSQL (`phones` table)
- ✅ API Server (FastAPI + Uvicorn)
  - `POST /ask` → compare phones or get details

---

## 🧰 Tech Stack

- Python
- Requests + BeautifulSoup (scraping)
- PostgreSQL (database)
- FastAPI + Uvicorn (API)

---

## 📁 Project Structure (example)

```txt
Task2-Samsung-Phone-Advisor/
├─ src/
│  ├─ api.py
│  ├─ agents.py
│  ├─ rag_db.py
│  ├─ db.py
│  ├─ scrape_phone_data.py
│  └─ scrape_one.py
├─ .venv/
└─ README.md
✅ Setup (One Time)
1) Create & activate virtual environment
bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
2) Install dependencies
If you have requirements.txt:

bash
Copy code
pip install -r requirements.txt
If not, install manually:

bash
Copy code
pip install requests beautifulsoup4 psycopg2-binary fastapi uvicorn
🗄️ PostgreSQL Setup
1) Create database
bash
Copy code
createdb samsung_db
2) Check DB connection
bash
Copy code
psql -U tayeebi -d samsung_db -c "SELECT 1;"
👀 Check What’s Saved in DB
Count rows
bash
Copy code
psql -U tayeebi -d samsung_db -c "SELECT COUNT(*) FROM phones;"
View latest 10 saved rows
bash
Copy code
psql -U tayeebi -d samsung_db -c "SELECT id, model_name, url, ram, storage, price, scraped_at FROM phones ORDER BY id DESC LIMIT 10;"
🧹 Reset / Delete Old Data (Optional)
⚠️ This deletes everything from phones and resets ID.

bash
Copy code
psql -U tayeebi -d samsung_db -c "TRUNCATE TABLE phones RESTART IDENTITY;"
Confirm it’s empty:

bash
Copy code
psql -U tayeebi -d samsung_db -c "SELECT COUNT(*) FROM phones;"
🕷️ Scrape Samsung Phones (20–30 phones)
Run the scraper:

bash
Copy code
python src/scrape_phone_data.py
Expected output example:

txt
Copy code
Reading list page 1...
Links found: 30
[1/30] Saved ✅: Samsung Galaxy A07
...
Done ✅ New saved: 30
Verify rows:

bash
Copy code
psql -U tayeebi -d samsung_db -c "SELECT COUNT(*) FROM phones;"
🚀 Run the API Server
Start FastAPI:

bash
Copy code
uvicorn src.api:app --reload
You should see:

txt
Copy code
Uvicorn running on http://127.0.0.1:8000
Open Swagger UI:

txt
Copy code
http://127.0.0.1:8000/docs
🧪 Test the API
1) Compare two phones
Request JSON

json
Copy code
{
  "question": "Compare S25 and S25+"
}
Curl command

bash
Copy code
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Compare S25 and S25+"}'
✅ Expected result:

If both phones exist in DB → returns a comparison answer

If not found → tells you to try a clearer model name

🛠️ Common Commands
Stop the server / stop running code
Press:

txt
Copy code
CTRL + C
Check if API is running
bash
Copy code
curl http://127.0.0.1:8000/
✅ Status
Scraper working ✅

Data inserted into DB ✅

API running ✅

/ask endpoint working ✅

pgsql
Copy code

If you want, paste your **current `src/agents.py` output formatting**, and I’ll rewrite it so `/ask` returns a **clean, nicely formatted text response** (not JSON-looking blocks).
::contentReference[oaicite:0]{index=0}