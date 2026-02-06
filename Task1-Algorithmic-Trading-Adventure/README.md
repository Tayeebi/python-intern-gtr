# 📈 Algorithmic Trading Adventure

**A beginner-friendly Python project that fetches market data, calculates indicators, and generates simple trading signals.**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](#)
[![Pandas](https://img.shields.io/badge/Pandas-DataFrame-success.svg)](#)
[![yfinance](https://img.shields.io/badge/yfinance-Market%20Data-orange.svg)](#)

---

## ✨ Overview

This task builds a simple end-to-end workflow (like a mini “trading bot” pipeline):

- ✅ Download historical stock price data
- ✅ Prepare and clean the dataset
- ✅ Calculate indicators (e.g., Moving Average)
- ✅ Generate trading signals (BUY / SELL / HOLD)
- ✅ *(Optional)* Run a basic backtest summary

---

## 🎯 Learning Goals

By completing this task, you will understand:

- What **market OHLCV data** looks like (Open/High/Low/Close/Volume)
- How to use **pandas** to work with data
- How indicators are computed (example: **SMA**)
- How a simple rule creates signals:
  - price crosses above → BUY
  - price crosses below → SELL

---

## 🧩 Tech Stack

| Tool | What it does (easy words) |
|------|----------------------------|
| Python | Runs the program |
| venv (`.venv`) | Keeps project packages separate from system Python |
| pip | Installs packages |
| pandas | Works like Excel tables, but in Python |
| yfinance | Downloads stock market data from Yahoo Finance |

---

## 📁 Project Structure

Typical structure (your project may look similar):

```txt
Task1-Algorithmic-Trading-Adventure/
├─ README.md
├─ requirements.txt
├─ main.py              # main runner (example)
└─ src/                 # (optional) code folder
   ├─ data.py
   ├─ strategy.py
   └─ main.py
```

---

## ✅ Prerequisites

- Python installed:
  ```bash
  python --version
  ```
- Internet connection (to download data using `yfinance`)

---

## ⚙️ Setup

> Run all commands inside your **Task 1 folder**.

### 1) Go to the Task 1 folder

```bash
cd /Users/tayeebi/Desktop/python-intern-gtr/Task1-Algorithmic-Trading-Adventure
```

### 2) Create a virtual environment (one time)

Why: it creates an isolated “box” for packages so nothing breaks your system Python.

```bash
python -m venv .venv
```

### 3) Activate the virtual environment

Why: now `pip` installs packages inside this project only.

```bash
source .venv/bin/activate
```

✅ You should now see `(.venv)` in your terminal.

### 4) Install dependencies

If you have `requirements.txt` (recommended):

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`:

```bash
pip install yfinance pandas
```

---

## ▶️ How to Run

### Option A: If you have `main.py` in the root folder

```bash
python main.py
```

### Option B: If your main file is inside `src/`

```bash
python src/main.py
```

### If you’re unsure what file to run

```bash
ls
```

Run the file that looks like `main.py`, `run.py`, or `task1.py`.

---

## 📌 Expected Output

Depending on your exact implementation, you may see:

- A preview of historical data (Date, Open, High, Low, Close, Volume)
- New indicator columns (examples):
  - `SMA_10`, `SMA_20`
- A signal column:
  - `BUY`, `SELL`, `HOLD`
- *(Optional)* backtest summary:
  - starting money
  - ending money
  - total profit/loss

---

## 🧪 Quick Health Checks

### 1) Confirm your Python is from `.venv`

```bash
which python
python --version
```

✅ It should show something like:

```txt
.../Task1-Algorithmic-Trading-Adventure/.venv/bin/python
```

### 2) Confirm packages work

```bash
python -c "import pandas, yfinance; print('OK ✅')"
```

---

## 🛠 Common Errors & Fixes

### ❌ `ModuleNotFoundError: No module named ...`

✅ Meaning: you ran Python outside the virtual environment.

Fix:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### ❌ `No such file or directory`

✅ Meaning: you are in the wrong folder OR using the wrong file path.

Fix:

```bash
pwd
ls
```

Then `cd` into the correct Task 1 folder and run the correct file.

---

## 📦 (Optional) Freeze dependencies

If you want to generate/update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## ✅ Submission Checklist

- [ ] `README.md`
- [ ] Python source files (`.py`)
- [ ] `requirements.txt`
- [ ] Output files (if your code generates any)

---
