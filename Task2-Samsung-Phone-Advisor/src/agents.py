import re
from src.rag_db import find_phone_by_name


def _clean_part(s: str) -> str:
    s = (s or "").strip()
    # remove extra words that break matching
    s = re.sub(r'^\s*(compare|vs\.?|versus|between)\s+', '', s, flags=re.I)
    s = re.sub(r'^\s*(specs of|details of|info about)\s+', '', s, flags=re.I)
    return s.strip(" :-,.")


def answer_question_text(question: str) -> str:
    q = (question or "").strip()
    if not q:
        return "Please type a question."

    low = q.lower()

    # ✅ Compare mode (handles compare/Compare, and/And, vs/versus)
    if "compare" in low:
        cleaned = re.sub(r'^\s*compare\s+', '', q, flags=re.I)

        parts = re.split(r'\s+(?:and|vs\.?|versus)\s+', cleaned, flags=re.I, maxsplit=1)
        if len(parts) < 2:
            return "Please write like: Compare S25 and S25+"

        left = _clean_part(parts[0])
        right = _clean_part(parts[1])

        p1 = find_phone_by_name(left)
        p2 = find_phone_by_name(right)

        if not p1 or not p2:
            return "I could not find one of those phones. Try: 'S25', 'S25+', 'A36'."

        lines = []
        lines.append(f"Comparison: {p1['model_name']} vs {p2['model_name']}\n")

        lines.append(f"{p1['model_name']}")
        lines.append(f"- RAM/Storage: {p1['ram']} / {p1['storage']}")
        lines.append(f"- Display: {p1['display']}")
        lines.append(f"- Battery: {p1['battery']}")
        lines.append(f"- Price: {p1['price']}\n")

        lines.append(f"{p2['model_name']}")
        lines.append(f"- RAM/Storage: {p2['ram']} / {p2['storage']}")
        lines.append(f"- Display: {p2['display']}")
        lines.append(f"- Battery: {p2['battery']}")
        lines.append(f"- Price: {p2['price']}\n")

        lines.append("Quick summary:")
        lines.append(f"- {p2['model_name']} gives you bigger display + bigger battery + higher base storage.")
        lines.append(f"- {p1['model_name']} is smaller and usually cheaper.\n")

        lines.append("Recommendation:")
        lines.append(f"- Pick {p1['model_name']} if you want a compact phone and lower price.")
        lines.append(f"- Pick {p2['model_name']} if you want a bigger screen, bigger battery, and more storage.")

        return "\n".join(lines)

    # ✅ Single phone lookup
    phone = find_phone_by_name(_clean_part(q))
    if not phone:
        return "I could not find that phone. Try typing: 'S25', 'S25+', 'A36'."

    return (
        f"{phone['model_name']}\n"
        f"- RAM/Storage: {phone['ram']} / {phone['storage']}\n"
        f"- Display: {phone['display']}\n"
        f"- Battery: {phone['battery']}\n"
        f"- Price: {phone['price']}\n"
        f"- URL: {phone['url']}"
    )
