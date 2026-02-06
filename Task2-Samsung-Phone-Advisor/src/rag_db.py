import psycopg2

DB_DSN = "dbname=samsung_db user=tayeebi"


def _clean(text: str) -> str:
    return (text or "").strip()


def normalize_model_name(q: str) -> str:
    """
    User may type: 'S25', 'S25+', 'A36', 'Samsung Galaxy S25'
    We convert small names into DB-friendly search text.
    """
    q = _clean(q)

    if not q:
        return ""

    low = q.lower()

    # If user already typed "samsung", keep it
    if "samsung" in low:
        return q

    # If user typed like "S25", "S25+", "A36", "M06", etc.
    # most Samsung phones in DB start with "Samsung Galaxy ..."
    # so we prefix "Samsung Galaxy "
    # (works for your current scraped data)
    return "Samsung Galaxy " + q


def find_phone_by_name(name: str):
    """
    Returns ONE best matching phone row or None.
    Uses ILIKE so it works even if user writes only part of the name.
    """
    name = normalize_model_name(name)
    if not name:
        return None

    db = psycopg2.connect(DB_DSN)
    cur = db.cursor()

    # Find best match
    cur.execute(
        """
        SELECT model_name, url, release_date, display, battery, camera, ram, storage, price, scraped_at
        FROM phones
        WHERE model_name ILIKE %s
        ORDER BY scraped_at DESC, id DESC
        LIMIT 1;
        """,
        (f"%{name}%",),
    )

    row = cur.fetchone()
    cur.close()
    db.close()

    if not row:
        return None

    return {
        "model_name": row[0],
        "url": row[1],
        "release_date": row[2],
        "display": row[3],
        "battery": row[4],
        "camera": row[5],
        "ram": row[6],
        "storage": row[7],
        "price": row[8],
        "scraped_at": str(row[9]),
    }
