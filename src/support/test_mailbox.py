from __future__ import annotations

import imaplib
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email import message_from_bytes
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from html import unescape


@dataclass
class MailProbeItem:
    uid: str
    subject: str
    from_: str
    date: str


@dataclass
class MailMessage:
    uid: str
    subject: str
    from_: str
    date: str
    text_body: str
    html_body: str


def _decode_header_value(value: str | None) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return str(value)


def mailbox_settings_from_env() -> dict:
    login = os.getenv("TEST_MAIL_LOGIN")
    password = os.getenv("TEST_MAIL_PASSWORD")
    host = os.getenv("TEST_MAIL_IMAP_HOST", "outlook.office365.com")
    port = int(os.getenv("TEST_MAIL_IMAP_PORT", "993"))
    folder = os.getenv("TEST_MAIL_FOLDER", "Inbox")

    if not login:
        raise RuntimeError("Environment variable 'TEST_MAIL_LOGIN' is not set")
    if not password:
        raise RuntimeError("Environment variable 'TEST_MAIL_PASSWORD' is not set")

    return {
        "login": login,
        "password": password,
        "host": host,
        "port": port,
        "folder": folder,
    }


def open_mailbox_from_env() -> imaplib.IMAP4_SSL:
    settings = mailbox_settings_from_env()
    mailbox = imaplib.IMAP4_SSL(settings["host"], settings["port"])
    mailbox.login(settings["login"], settings["password"])
    status, _ = mailbox.select(settings["folder"])
    if status != "OK":
        mailbox.logout()
        raise RuntimeError(f"Failed to select folder '{settings['folder']}'")
    return mailbox


def _fetch_raw_message(mailbox: imaplib.IMAP4_SSL, uid: str) -> bytes | None:
    fetch_status, fetch_data = mailbox.uid("fetch", uid, "(RFC822)")
    if fetch_status != "OK" or not fetch_data:
        return None

    for chunk in fetch_data:
        if isinstance(chunk, tuple) and len(chunk) >= 2:
            return chunk[1]
    return None


def _extract_bodies(message) -> tuple[str, str]:
    text_parts: list[str] = []
    html_parts: list[str] = []

    if message.is_multipart():
        for part in message.walk():
            content_type = str(part.get_content_type() or "").lower()
            disposition = str(part.get("Content-Disposition") or "").lower()
            if "attachment" in disposition:
                continue

            payload = part.get_payload(decode=True)
            if payload is None:
                continue

            charset = part.get_content_charset() or "utf-8"
            try:
                content = payload.decode(charset, errors="replace")
            except Exception:
                content = payload.decode("utf-8", errors="replace")

            if content_type == "text/plain":
                text_parts.append(content)
            elif content_type == "text/html":
                html_parts.append(content)
    else:
        payload = message.get_payload(decode=True)
        if payload is not None:
            charset = message.get_content_charset() or "utf-8"
            try:
                content = payload.decode(charset, errors="replace")
            except Exception:
                content = payload.decode("utf-8", errors="replace")

            content_type = str(message.get_content_type() or "").lower()
            if content_type == "text/html":
                html_parts.append(content)
            else:
                text_parts.append(content)

    return "\n".join(text_parts).strip(), "\n".join(html_parts).strip()


def list_latest_messages(*, limit: int = 10) -> list[MailProbeItem]:
    mailbox = open_mailbox_from_env()
    try:
        status, data = mailbox.uid("search", None, "ALL")
        if status != "OK":
            raise RuntimeError("Failed to search mailbox")

        uids = [item.decode() for item in (data[0] or b"").split() if item]
        latest = list(reversed(uids[-limit:]))
        result: list[MailProbeItem] = []

        for uid in latest:
            raw_message = _fetch_raw_message(mailbox, uid)
            if not raw_message:
                continue

            message = message_from_bytes(raw_message)
            result.append(
                MailProbeItem(
                    uid=uid,
                    subject=_decode_header_value(message.get("Subject")),
                    from_=_decode_header_value(message.get("From")),
                    date=_decode_header_value(message.get("Date")),
                )
            )

        return result
    finally:
        try:
            mailbox.close()
        except Exception:
            pass
        mailbox.logout()


def get_message_by_uid(uid: str) -> MailMessage:
    mailbox = open_mailbox_from_env()
    try:
        raw_message = _fetch_raw_message(mailbox, uid)
        if not raw_message:
            raise RuntimeError(f"Message UID={uid} not found")

        message = message_from_bytes(raw_message)
        text_body, html_body = _extract_bodies(message)
        return MailMessage(
            uid=uid,
            subject=_decode_header_value(message.get("Subject")),
            from_=_decode_header_value(message.get("From")),
            date=_decode_header_value(message.get("Date")),
            text_body=text_body,
            html_body=html_body,
        )
    finally:
        try:
            mailbox.close()
        except Exception:
            pass
        mailbox.logout()


def find_latest_message(
    *,
    subject_contains: str | None = None,
    from_contains: str | None = None,
    limit: int = 20,
) -> MailProbeItem | None:
    items = list_latest_messages(limit=limit)
    for item in items:
        if subject_contains and subject_contains.lower() not in item.subject.lower():
            continue
        if from_contains and from_contains.lower() not in item.from_.lower():
            continue
        return item
    return None


def extract_urls_from_message(message: MailMessage) -> list[str]:
    body = "\n".join(part for part in [message.text_body, unescape(message.html_body)] if part).strip()
    if not body:
        return []
    return re.findall(r"https?://[^\s\"'<>]+", body)


def _parse_mail_datetime(date_header: str) -> datetime | None:
    if not date_header:
        return None
    try:
        parsed = parsedate_to_datetime(date_header)
    except Exception:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def find_fresh_verification_email(*, started_at: datetime, limit: int = 20) -> MailProbeItem | None:
    started_at_utc = started_at.astimezone(timezone.utc) - timedelta(minutes=3)
    for item in list_latest_messages(limit=limit):
        subject = (item.subject or "").lower()
        sender = (item.from_ or "").lower()
        if "myqr" not in sender and "подтверж" not in subject and "confirm" not in subject:
            continue
        mail_dt = _parse_mail_datetime(item.date)
        if mail_dt and mail_dt < started_at_utc:
            continue
        return item
    return None


def choose_confirm_url(urls: list[str]) -> str | None:
    for url in urls:
        if "/accountactions/confirm/" in url.lower():
            return url
    for url in urls:
        lower = url.lower()
        if "confirm" in lower or "accountactions" in lower:
            return url
    return urls[0] if urls else None
