# UCLA Seat Checker

A small Python script that monitors UCLA Schedule of Classes endpoints and emails you when a monitored class has:

- an open seat, or
- an open waitlist spot.

Once a class triggers an alert, it is removed from the watch list for that run.

## How It Works

`seat_checker.py`:

- checks each class URL in `CLASSES`
- tries to detect seat and waitlist availability from API/HTML responses
- sends an email alert via Gmail SMTP
- repeats every `CHECK_INTERVAL` seconds until all monitored classes have alerted

## Requirements

- Python 3.9+
- A Gmail account with an App Password (recommended)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Add classes to monitor

Edit the `CLASSES` dictionary in `seat_checker.py`.

Each key is the display name, and each value is the UCLA endpoint URL for that class.

### 2. Set environment variables

The script reads these variables:

- `EMAIL_USER`: sender Gmail address
- `EMAIL_PASS`: Gmail App Password
- `ALERT_TO`: recipient email address
- `CHECK_INTERVAL`: polling interval in seconds (optional, default `60`)

Set them in your shell, for example:

```bash
export EMAIL_USER="you@gmail.com"
export EMAIL_PASS="your_app_password"
export ALERT_TO="you@gmail.com"
export CHECK_INTERVAL="60"
```

Notes:

- `load_dotenv()` is currently commented out in `seat_checker.py`, so `.env` files are not loaded unless you uncomment that line.
- For Gmail, use an App Password instead of your normal account password.

## Run

```bash
python seat_checker.py
```

The script will keep running until every monitored class has triggered an alert.

## Example Output

```text
Starting UCLA seat checker...
[ENGR 111] seats_available=0 wait_available=0
Waiting 60s before next check...
```

When availability is found, it sends an email and logs which class triggered.

## Files

- `seat_checker.py`: main monitoring script
- `requirements.txt`: Python dependencies
- `cs131_response.html`: sample response artifact used during development/debugging

## Troubleshooting

- If no alerts are sent, verify `EMAIL_USER`, `EMAIL_PASS`, and `ALERT_TO` are set in the shell where you run the script.
- If Gmail login fails, ensure 2FA is enabled and the App Password is correct.
- If availability detection seems wrong, print/save the raw response and adjust parsing logic in `check_class()`.

## Disclaimer

This project is for personal use and convenience. UCLA endpoint formats may change, which can break parsing logic and require updates.
