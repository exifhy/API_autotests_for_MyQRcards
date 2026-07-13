import imaplib
import email
import time
import os
from datetime import datetime, timezone
from email.header import decode_header
from dotenv import load_dotenv
from loguru import logger
from utils.helper import Helper

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = os.getenv("IMAP_PORT")
EMAIL_LOGIN = os.getenv("LOGIN_EMAIL")
EMAIL_PASSWORD = os.getenv("PASSWORD_EMAIL")


def decode_mime_words(s):
    decoded = decode_header(s)
    return ''.join(
        str(part[0], part[1] or 'utf-8') if isinstance(part[0], bytes) else part[0]
        for part in decoded
    )


def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        return msg.get_payload(decode=True).decode(errors="ignore")
    return ""


def parse_email_date(date_str):
    """Преобразует дату письма в UTC datetime"""
    parsed = email.utils.parsedate_to_datetime(date_str)
    return parsed.astimezone(timezone.utc)


def wait_for_email(request_id: str, start_time: datetime, expected_subject: str, expected_body: str):

    timeout = 5 * 60
    poll_interval = 30

    logger.info("Waiting time before the first check (31 seconds)...")
    Helper.sleep_with_progress_bar(31)

    start_ts = start_time.astimezone(timezone.utc)

    logger.info(f"Beginning of mail verification (task number={request_id})")

    while True:
        elapsed = (datetime.now(timezone.utc) - start_ts).total_seconds()

        logger.debug(f"Time has passed: {elapsed:.1f} sec")

        if elapsed > timeout:
            logger.error("Timeout 5 min exceeded")
            return False, "Timeout 5 min exceeded"

        try:
            logger.debug("Connecting to IMAP...")
            mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
            mail.login(EMAIL_LOGIN, EMAIL_PASSWORD)
            mail.select("INBOX")

            status, messages = mail.search(None, '(FROM "no-reply@hubex.ru")')
            mail_ids = messages[0].split()

            logger.debug(f"Found emails from the sender: {len(mail_ids)}")

            for mail_id in reversed(mail_ids):
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                # 📅 фильтр по времени
                msg_date = parse_email_date(msg.get("Date"))
                if msg_date < start_ts:
                    continue

                subject = decode_mime_words(msg.get("Subject", ""))
                logger.debug(f"Check email: subject='{subject}'")

                if subject != expected_subject:
                    continue

                logger.info("An email with the desired subject was found")

                body = get_email_body(msg)

                if expected_body not in body:
                    logger.error(f"The subject matches, but the body of the email is invalid. {body}")
                    return False, "Subject matched but body validation failed"

                if expected_body in body:
                    logger.success("The email was found and validated")
                    return True, "Email validated"

        except Exception as e:
            logger.exception(f"Error IMAP: {e}")
            return False, f"IMAP error: {e}"
        
        logger.info(f"The next check is in {poll_interval} sec...")
        time.sleep(poll_interval)