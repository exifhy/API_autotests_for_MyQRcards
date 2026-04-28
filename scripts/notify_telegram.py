import os
import re
import sys
from datetime import datetime, timezone, timedelta

import requests

MOSCOW = timezone(timedelta(hours=3))


def parse_pytest_output(path: str) -> tuple[str, int, int]:
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return "no output", 0, 0

    match = re.search(r"(\d+) passed", text)
    passed = int(match.group(1)) if match else 0

    match = re.search(r"(\d+) failed", text)
    failed = int(match.group(1)) if match else 0

    matches = re.findall(r"=+ (.+?) =+", text)
    summary = matches[-1].strip() if matches else "unknown"

    return summary, passed, failed


def failed_tests(path: str, limit: int = 10) -> list[str]:
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return []
    return re.findall(r"FAILED (tests/\S+)", text)[:limit]


def send(token: str, chat_id: str, text: str) -> None:
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=15,
    )


def main() -> None:
    output_file = sys.argv[1] if len(sys.argv) > 1 else "pytest_output.txt"
    env_label = sys.argv[2] if len(sys.argv) > 2 else "DEV"

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return

    summary, passed, failed = parse_pytest_output(output_file)
    now = datetime.now(MOSCOW).strftime("%Y-%m-%d %H:%M")

    if failed == 0 and passed > 0:
        icon = "✅"
        status = "PASSED"
    elif failed > 0:
        icon = "❌"
        status = "FAILED"
    else:
        icon = "⚠️"
        status = "NO RESULTS"

    allure_url = os.environ.get("ALLURE_URL", "")

    lines = [
        f"{icon} <b>{env_label} smoke — {status}</b>",
        f"📊 {summary}",
        f"🕐 {now} (Moscow)",
    ]
    if allure_url:
        lines.append(f'📋 <a href="{allure_url}">Allure report</a>')

    if failed > 0:
        failures = failed_tests(output_file)
        if failures:
            lines.append("\n<b>Упавшие тесты:</b>")
            for t in failures:
                lines.append(f"• <code>{t}</code>")

    send(token, chat_id, "\n".join(lines))
    print("Telegram notification sent")


if __name__ == "__main__":
    main()
