import time
import requests
import os
import smtplib
from email.message import EmailMessage

# =======================
# CONFIG — ADD CLASSES HERE
# =======================

CLASSES = {
    "ENGR 111": (
        "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary"
        "?model=%7B%22Term%22%3A%2226W%22%2C%22SubjectAreaCode%22%3A%22ENGR+++%22%2C%22CatalogNumber%22%3A%220111++++%22%2C%22IsRoot%22%3Atrue%2C%22SessionGroup%22%3A%22%25%22%2C%22ClassNumber%22%3A%22%25%22%2C%22SequenceNumber%22%3Anull%2C%22Path%22%3A%22ENGR0111%22%2C%22MultiListedClassFlag%22%3A%22n%22%2C%22Token%22%3A%22MDExMSAgICBFTkdSMDExMQ%3D%3D%22%7D"
        "&FilterFlags=%7B%22enrollment_status%22%3A%22O%2CW%2CC%2CX%2CT%2CS%22%2C%22advanced%22%3A%22y%22%2C%22meet_days%22%3A%22M%2CT%2CW%2CR%2CF%22%2C%22start_time%22%3A%228%3A00+am%22%2C%22end_time%22%3A%228%3A00+pm%22%7D"
    ),
}

# =======================
# EMAIL / ENV
# =======================

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ALERT_TO = os.getenv("ALERT_TO")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

# =======================
# EMAIL
# =======================

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["From"] = EMAIL_USER
    msg["To"] = ALERT_TO
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

# =======================
# CHECK ONE CLASS
# =======================

def check_class(class_name, url):
    response = requests.get(url, timeout=15)
    text = response.text.lower()

    seat_open = "open" in text and "class full" not in text
    waitlist_open = "waitlist" in text and "no waitlist" not in text

    print(f"[{class_name}]")
    print(text.strip()[:200], "\n")

    if seat_open:
        return "seat"
    if waitlist_open:
        return "waitlist"

    return None

# =======================
# MAIN LOOP
# =======================

def main():
    print("Starting UCLA seat checker...\n")

    pending = dict(CLASSES)  # copy

    while pending:
        for class_name, url in list(pending.items()):
            try:
                status = check_class(class_name, url)

                if status == "seat":
                    send_email(
                        f"🎉 SEAT OPEN — {class_name}",
                        f"A SEAT is now OPEN for {class_name}.\n\n"
                        "Enroll immediately:\nhttps://sa.ucla.edu/ro/public/soc"
                    )
                    print(f"{class_name}: seat open — alerted.\n")
                    pending.pop(class_name)

                elif status == "waitlist":
                    send_email(
                        f"⏳ WAITLIST OPEN — {class_name}",
                        f"The WAITLIST is now OPEN for {class_name}.\n\n"
                        "Enroll immediately:\nhttps://sa.ucla.edu/ro/public/soc"
                    )
                    print(f"{class_name}: waitlist open — alerted.\n")
                    pending.pop(class_name)

            except Exception as e:
                print(f"{class_name}: error — {e}")

        if pending:
            print(f"Waiting {CHECK_INTERVAL}s before next check...\n")
            time.sleep(CHECK_INTERVAL)

    print("All monitored classes triggered — exiting.")

if __name__ == "__main__":
    main()
