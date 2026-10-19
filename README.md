# Security Log Analyzer

A beginner-friendly Python + Tkinter cybersecurity portfolio project.

## Features
- Demo login screen
- Dashboard showing total, successful, and failed login attempts
- Reads sample logs from `login_logs.txt`
- Searches log entries by timestamp, username, IP address, or status
- Alerts when an IP address has 3 or more failed login attempts
- No third-party packages required (uses Python's built-in Tkinter)

## Files
- `security_log_analyzer.py` — application code
- `login_logs.txt` — sample log data
- `README.md` — instructions

## Run on Windows
1. Keep both files in the same folder.
2. Open Command Prompt in that folder.
3. Run:
   `python security_log_analyzer.py`

## Demo login
- Username: `admin`
- Password: `analyzer123`

This is a learning/demo login only, not secure authentication for real accounts.

## Expected sample result
- Total login attempts: 8
- Successful logins: 4
- Failed logins: 4
- Alert: `203.0.113.25 - 3 failed attempts`

The sample IP addresses use documentation-only ranges; they are not intended to identify real users. Only analyze logs you are authorized to access.
