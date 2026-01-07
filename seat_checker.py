import time
import requests
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# =======================
# CONFIG (EDIT ONLY THIS)
# =======================

CLASS_NAME = "ENGR 111"

REQUEST_URL = (
    "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary"
    "?model=%7B%22Term%22%3A%2226W%22%2C%22SubjectAreaCode%22%3A%22ENGR+++%22%2C%22CatalogNumber%22%3A%220111++++%22%2C%22IsRoot%22%3Atrue%2C%22SessionGroup%22%3A%22%25%22%2C%22ClassNumber%22%3A%22%25%22%2C%22SequenceNumber%22%3Anull%2C%22Path%22%3A%22ENGR0111%22%2C%22MultiListedClassFlag%22%3A%22n%22%2C%22Token%22%3A%22MDExMSAgICBFTkdSMDExMQ%3D%3D%22%7D"
    "&FilterFlags=%7B%22enrollment_status%22%3A%22O%2CW%2CC%2CX%2CT%2CS%22%2C%22advanced%22%3A%22y%22%2C%22meet_days%22%3A%22M%2CT%2CW%2CR%2CF%22%2C%22start_time%22%3A%228%3A00+am%22%2C%22end_time%22%3A%228%3A00+pm%22%7D"
)

# =======================
# ENV / EMAIL SETTINGS
# =======================

load_dotenv()

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ALERT_TO = os.getenv("ALERT_TO")


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
# CHECK AVAILABILITY
# =======================

def check_availability():
    response = requests.get(REQUEST_URL, timeout=15)
    text = response.text.lower()

    seat_open = "open" in text and "class full" not in text
    waitlist_open = "waitlist" in text and "no waitlist" not in text

    print(f"[{CLASS_NAME}] status:")
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
    print(f"Monitoring {CLASS_NAME}...\n")

    while True:
        try:
            status = check_availability()

            if status == "seat":
                send_email(
                    f"🎉 SEAT OPEN — {CLASS_NAME}",
                    f"A SEAT is now OPEN for {CLASS_NAME}.\n\n"
                    f"Enroll immediately:\nhttps://sa.ucla.edu/ro/public/soc"
                )
                print("Seat available — notification sent.")
                break

            if status == "waitlist":
                send_email(
                    f"⏳ WAITLIST OPEN — {CLASS_NAME}",
                    f"The WAITLIST is now OPEN for {CLASS_NAME}.\n\n"
                    f"Enroll immediately:\nhttps://sa.ucla.edu/ro/public/soc"
                )
                print("Waitlist available — notification sent.")
                break

        except Exception as e:
            print("Error:", e)

        print(f"No availability. Checking again in {CHECK_INTERVAL}s...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
