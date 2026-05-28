from __future__ import annotations

import argparse

from src.config.env_loader import load_env
from src.support.test_mailbox import list_latest_messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe test mailbox via IMAP")
    parser.add_argument("--env", default="dev", choices=["dev", "prod"])
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    load_env(args.env)
    items = list_latest_messages(limit=args.limit)
    print(f"Mailbox probe OK. Last {len(items)} message(s):")
    for item in items:
        print(f"- UID={item.uid} | Date={item.date} | From={item.from_} | Subject={item.subject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
