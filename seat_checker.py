import time
import requests
import os
import smtplib
from email.message import EmailMessage
import re
from dotenv import load_dotenv

# =======================
# CONFIG — ADD CLASSES HERE
# =======================

CLASSES = {
    "ENGR 111": (
        "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary"
        "?model=%7B%22Term%22%3A%2226W%22%2C%22SubjectAreaCode%22%3A%22ENGR+++%22%2C%22CatalogNumber%22%3A%220111++++%22%2C%22IsRoot%22%3Atrue%2C%22SessionGroup%22%3A%22%25%22%2C%22ClassNumber%22%3A%22%25%22%2C%22SequenceNumber%22%3Anull%2C%22Path%22%3A%22ENGR0111%22%2C%22MultiListedClassFlag%22%3A%22n%22%2C%22Token%22%3A%22MDExMSAgICBFTkdSMDExMQ%3D%3D%22%7D"
        "&FilterFlags=%7B%22enrollment_status%22%3A%22O%2CW%2CC%2CX%2CT%2CS%22%2C%22advanced%22%3A%22y%22%2C%22meet_days%22%3A%22M%2CT%2CW%2CR%2CF%22%2C%22start_time%22%3A%228%3A00+am%22%2C%22end_time%22%3A%228%3A00+pm%22%7D"
    ),
    "COM SCI M146": (
        "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary"
        "?model=%7B%22Term%22%3A%2226W%22%2C%22SubjectAreaCode%22%3A%22COM+SCI%22%2C%22CatalogNumber%22%3A%220146++M+%22%2C%22IsRoot%22%3Atrue%2C%22SessionGroup%22%3A%22%25%22%2C%22ClassNumber%22%3A%22%25%22%2C%22SequenceNumber%22%3Anull%2C%22Path%22%3A%22COMSCI0146M%22%2C%22MultiListedClassFlag%22%3A%22y%22%2C%22Token%22%3A%22MDE0NiAgTSBDT01TQ0kwMTQ2TQ%3D%3D%22%7D&FilterFlags=%7B%22enrollment_status%22%3A%22O%2CW%2CC%2CX%2CT%2CS%22%2C%22advanced%22%3A%22y%22%2C%22meet_days%22%3A%22M%2CT%2CW%2CR%2CF%22%2C%22start_time%22%3A%228%3A00+am%22%2C%22end_time%22%3A%228%3A00+pm%22%2C%22meet_locations%22%3Anull%2C%22meet_units%22%3Anull%2C%22instructor%22%3Anull%2C%22class_career%22%3Anull%2C%22impacted%22%3Anull%2C%22enrollment_restrictions%22%3Anull%2C%22enforced_requisites%22%3Anull%2C%22individual_studies%22%3Anull%2C%22summer_session%22%3Anull%7D&_=1767827962001"
    ),
    "EL ENGR C147A": (
        "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary"
        "?model=%7B%22Term%22%3A%2226W%22%2C%22SubjectAreaCode%22%3A%22EC+ENGR%22%2C%22CatalogNumber%22%3A%220147A+C+%22%2C%22IsRoot%22%3Atrue%2C%22SessionGroup%22%3A%22%25%22%2C%22ClassNumber%22%3A%22%25%22%2C%22SequenceNumber%22%3Anull%2C%22Path%22%3A%22ECENGR0147AC%22%2C%22MultiListedClassFlag%22%3A%22n%22%2C%22Token%22%3A%22MDE0N0EgQyBFQ0VOR1IwMTQ3QUM%3D%22%7D&FilterFlags=%7B%22enrollment_status%22%3A%22O%2CW%2CC%2CX%2CT%2CS%22%2C%22advanced%22%3A%22y%22%2C%22meet_days%22%3A%22M%2CT%2CW%2CR%2CF%22%2C%22start_time%22%3A%228%3A00+am%22%2C%22end_time%22%3A%228%3A00+pm%22%2C%22meet_locations%22%3Anull%2C%22meet_units%22%3Anull%2C%22instructor%22%3Anull%2C%22class_career%22%3Anull%2C%22impacted%22%3Anull%2C%22enrollment_restrictions%22%3Anull%2C%22enforced_requisites%22%3Anull%2C%22individual_studies%22%3Anull%2C%22summer_session%22%3Anull%7D&_=1767828073806"
    ),
    "LING 1": (
        "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary?"
        "model=%7B%22Term%22%3A%2226W%22%2C%22SubjectAreaCode%22%3A%22LING+++%22%2C%22CatalogNumber%22%3A%220001++++%22%2C%22IsRoot%22%3Atrue%2C%22SessionGroup%22%3A%22%25%22%2C%22ClassNumber%22%3A%22%25%22%2C%22SequenceNumber%22%3Anull%2C%22Path%22%3A%22LING0001%22%2C%22MultiListedClassFlag%22%3A%22n%22%2C%22Token%22%3A%22MDAwMSAgICBMSU5HMDAwMQ%3D%3D%22%7D&FilterFlags=%7B%22enrollment_status%22%3A%22O%2CW%2CC%2CX%2CT%2CS%22%2C%22advanced%22%3A%22y%22%2C%22meet_days%22%3A%22M%2CT%2CW%2CR%2CF%22%2C%22start_time%22%3A%228%3A00+am%22%2C%22end_time%22%3A%227%3A00+pm%22%2C%22meet_locations%22%3Anull%2C%22meet_units%22%3Anull%2C%22instructor%22%3Anull%2C%22class_career%22%3Anull%2C%22impacted%22%3A%22N%22%2C%22enrollment_restrictions%22%3Anull%2C%22enforced_requisites%22%3Anull%2C%22individual_studies%22%3Anull%2C%22summer_session%22%3Anull%7D&_=1767831222020"
    ),
}

# =======================
# EMAIL / ENV
# =======================

# load_dotenv()

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
    text = response.text or ""
    lower = text.lower()

    # Prefer JSON parsing if the endpoint returns JSON
    seats_available = None
    wait_available = None

    # Try to parse JSON body
    json_data = None
    try:
        # Some endpoints return JSON; .json() will raise if not
        json_data = response.json()
    except Exception:
        json_data = None

    def find_numbers(obj):
        """Recursively search JSON for likely seat/wait numeric fields."""
        out = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                lk = k.lower()
                if isinstance(v, (int, float)):
                    if 'seat' in lk and ('avail' in lk or 'available' in lk):
                        out['seats_available'] = int(v)
                    if 'wait' in lk and ('avail' in lk or 'available' in lk):
                        out['wait_available'] = int(v)
                    if 'enrolled' in lk and 'wait' not in lk:
                        out['seats_enrolled'] = int(v)
                    if ('capacity' in lk or 'cap' in lk) and 'wait' not in lk:
                        out['seats_capacity'] = int(v)
                else:
                    nested = find_numbers(v)
                    for nk, nv in nested.items():
                        if nk not in out:
                            out[nk] = nv
        elif isinstance(obj, list):
            for item in obj:
                nested = find_numbers(item)
                for nk, nv in nested.items():
                    if nk not in out:
                        out[nk] = nv
        return out

    if json_data is not None:
        nums = find_numbers(json_data)
        seats_available = nums.get('seats_available')
        wait_available = nums.get('wait_available')
        # If we have enrolled/capacity, derive availability
        if seats_available is None and 'seats_enrolled' in nums and 'seats_capacity' in nums:
            seats_available = max(0, nums['seats_capacity'] - nums['seats_enrolled'])

    # -----------------------------
    # SEAT AVAILABILITY DETECTION
    # -----------------------------
    seats_available = None
    orig = text

    # 1) Try explicit "Seats Available: N"
    m = re.search(r'seats\s*(?:available|avail)[:\s]*([0-9]+)', orig, re.I)
    if m:
        seats_available = int(m.group(1))

    # 2) Try "X Spots Left" or "X Seats Left"
    if seats_available is None:
        m_spots = re.search(r'(\d+)\s*(?:spots?|seats?)\s*(?:left|remaining)?', orig, re.I)
        if m_spots:
            seats_available = int(m_spots.group(1))

    # 3) Try "Y of Z Enrolled" -> capacity - enrolled
    if seats_available is None:
        m_enrolled = re.search(r'(\d+)\s*of\s*(\d+)\s*enrolled', orig, re.I)
        if m_enrolled:
            try:
                enrolled = int(m_enrolled.group(1))
                capacity = int(m_enrolled.group(2))
                seats_available = max(0, capacity - enrolled)
            except Exception:
                seats_available = None

    # 4) Try "N remaining/left" near the words seat/enroll/spots
    if seats_available is None:
        for m_rem in re.finditer(r'(\d+)\s*(?:remaining|left)', orig, re.I):
            ctx_start = max(0, m_rem.start() - 40)
            ctx_end = min(len(orig), m_rem.end() + 40)
            ctx = orig[ctx_start:ctx_end].lower()
            if 'seat' in ctx or 'enroll' in ctx or 'spots' in ctx:
                try:
                    seats_available = int(m_rem.group(1))
                    break
                except Exception:
                    continue

    # 5) Negative indicators
    if seats_available is None:
        if 'class full' in lower or 'closed' in lower or 'no seats' in lower:
            seats_available = 0

    # 6) Optional weak textual fallback (disabled by default)
    USE_WEAK_OPEN_FALLBACK = False
    if seats_available is None and USE_WEAK_OPEN_FALLBACK:
        if 'open' in lower and 'class full' not in lower and 'closed' not in lower:
            seats_available = 1  # assume at least one seat

    # Determine seat open state
    seat_open = False
    if seats_available is not None:
        seat_open = seats_available > 0

    # Now evaluate waitlist state (don't let 'No Waitlist' short-circuit useful numeric detection)
    if wait_available is None:
        # find numeric waitlist availability like "Waitlist Available: N"
        m = re.search(r'waitlist\s*(available|avail)[:\s]*([0-9]+)', lower)
        if m:
            wait_available = int(m.group(2))
        else:
            # Try to parse patterns like "9 of 10 Taken" that often follow a "Waitlist" label
            frac_pattern = re.compile(r"(\d+)\s*of\s*(\d+)\s*(?:taken|taken\.|available)?", re.I)
            for fm in frac_pattern.finditer(text):
                # look around the match for the word 'wait' to decide if it's a waitlist fraction
                ctx_start = max(0, fm.start() - 50)
                ctx_end = min(len(text), fm.end() + 50)
                ctx = text[ctx_start:ctx_end].lower()
                if 'wait' in ctx:
                    try:
                        enrolled = int(fm.group(1))
                        capacity = int(fm.group(2))
                        wait_available = max(0, capacity - enrolled)
                        break
                    except Exception:
                        continue

            # If still unknown, consider explicit 'No Waitlist' as zero; otherwise be conservative
            if wait_available is None:
                if re.search(r'no\s*waitlist', lower):
                    wait_available = 0
                elif 'waitlist' in lower:
                    # 'waitlist' word present but no numeric info: assume closed (0) to avoid false positives
                    wait_available = 0

    # Determine waitlist state (prefer numeric indicators)
    waitlist_open = False
    if wait_available is not None:
        waitlist_open = wait_available > 0
    else:
        waitlist_open = False

    print(f"[{class_name}] seats_available={seats_available} wait_available={wait_available}")
    print(lower.strip()[:200], "\n")

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
