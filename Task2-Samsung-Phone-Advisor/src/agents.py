from src.rag_db import find_phone_by_name


def answer_question_text(question: str) -> str:
    q = (question or "").strip()
    if not q:
        return "Please type a question."

    low = q.lower()

    # compare mode
    if "compare" in low and "and" in low:
        parts = q.replace("Compare", "").split("and")
        left = parts[0].strip()
        right = parts[1].strip()

        p1 = find_phone_by_name(left)
        p2 = find_phone_by_name(right)

        if not p1 or not p2:
            return "I could not find one of those phones. Try: 'S25', 'S25+', 'A36'."

        # smooth organized text
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

    # single phone mode
    phone = find_phone_by_name(q)
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
