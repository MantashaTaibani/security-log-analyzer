import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter

APP_TITLE = "Security Log Analyzer"
LOG_FILE = "login_logs.txt"
FAILED_THRESHOLD = 3

# Demo-only login. Do not use these credentials for a real account.
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "analyzer123"


def read_logs():
    records = []
    if not os.path.exists(LOG_FILE):
        messagebox.showerror(
            "Log file missing",
            f"Could not find {LOG_FILE}.\nKeep it in the same folder as this program."
        )
        return records

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("|")
            if len(parts) != 4:
                continue

            timestamp, username, ip_address, status = [part.strip() for part in parts]
            records.append({
                "timestamp": timestamp,
                "username": username,
                "ip": ip_address,
                "status": status.upper()
            })
    return records


def analyze_logs():
    records = read_logs()
    if not records:
        return

    successful = sum(1 for item in records if item["status"] == "SUCCESS")
    failed = sum(1 for item in records if item["status"] == "FAILED")
    failed_by_ip = Counter(
        item["ip"] for item in records if item["status"] == "FAILED"
    )

    for row in log_table.get_children():
        log_table.delete(row)

    for item in records:
        log_table.insert(
            "",
            "end",
            values=(item["timestamp"], item["username"], item["ip"], item["status"])
        )

    total_value.config(text=str(len(records)))
    success_value.config(text=str(successful))
    failed_value.config(text=str(failed))

    alerts = [
        f"{ip_address} - {count} failed attempts"
        for ip_address, count in failed_by_ip.items()
        if count >= FAILED_THRESHOLD
    ]

    alert_text.config(state="normal")
    alert_text.delete("1.0", "end")
    if alerts:
        for alert in alerts:
            alert_text.insert("end", "ALERT: " + alert + "\n")
    else:
        alert_text.insert("end", "No IP addresses reached the alert threshold.\n")
    alert_text.config(state="disabled")

    status_label.config(text=f"Analysis completed. Read {len(records)} log entries.")


def filter_logs(*args):
    search_term = search_var.get().strip().lower()
    for row in log_table.get_children():
        log_table.delete(row)

    records = read_logs()
    for item in records:
        combined = " ".join([
            item["timestamp"], item["username"], item["ip"], item["status"]
        ]).lower()
        if search_term in combined:
            log_table.insert(
                "", "end",
                values=(item["timestamp"], item["username"], item["ip"], item["status"])
            )


def show_dashboard():
    login_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)
    analyze_logs()


def login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if username == DEMO_USERNAME and password == DEMO_PASSWORD:
        show_dashboard()
    else:
        messagebox.showerror("Login failed", "Incorrect username or password.")


def logout():
    dashboard_frame.pack_forget()
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")
    login_frame.pack(fill="both", expand=True)


import os

root = tk.Tk()
root.title(APP_TITLE)
root.geometry("950x650")
root.minsize(800, 550)
root.configure(bg="#f3eadc")

style = ttk.Style()
try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure("TFrame", background="#f3eadc")
style.configure("TLabel", background="#f3eadc", foreground="#4b3325", font=("Segoe UI", 10))
style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#4b3325")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=7)
style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)
style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

login_frame = ttk.Frame(root, padding=35)
login_title = ttk.Label(login_frame, text="SECURITY LOG ANALYZER", style="Title.TLabel")
login_title.pack(pady=(65, 8))
ttk.Label(login_frame, text="Sign in to review login activity").pack(pady=(0, 25))

ttk.Label(login_frame, text="Username").pack()
username_entry = ttk.Entry(login_frame, width=32)
username_entry.pack(pady=(5, 15))
ttk.Label(login_frame, text="Password").pack()
password_entry = ttk.Entry(login_frame, width=32, show="*")
password_entry.pack(pady=(5, 20))
ttk.Button(login_frame, text="Login", command=login).pack()
ttk.Label(
    login_frame,
    text="Demo login: admin  |  Password: analyzer123",
    foreground="#7b6250"
).pack(pady=15)
login_frame.pack(fill="both", expand=True)

dashboard_frame = ttk.Frame(root, padding=15)

header = ttk.Frame(dashboard_frame)
header.pack(fill="x", pady=(0, 12))
ttk.Label(header, text="Security Dashboard", style="Title.TLabel").pack(side="left")
ttk.Button(header, text="Logout", command=logout).pack(side="right")

summary_frame = ttk.Frame(dashboard_frame)
summary_frame.pack(fill="x", pady=(0, 12))

def make_summary_card(parent, title, initial):
    card = tk.Frame(parent, bg="#e4d1bb", padx=18, pady=12, highlightbackground="#b79a7d", highlightthickness=1)
    tk.Label(card, text=title, bg="#e4d1bb", fg="#5b3d2a", font=("Segoe UI", 10)).pack()
    value = tk.Label(card, text=initial, bg="#e4d1bb", fg="#3b281d", font=("Segoe UI", 21, "bold"))
    value.pack(pady=(4, 0))
    card.pack(side="left", fill="x", expand=True, padx=5)
    return value

total_value = make_summary_card(summary_frame, "Total Attempts", "0")
success_value = make_summary_card(summary_frame, "Successful", "0")
failed_value = make_summary_card(summary_frame, "Failed", "0")

search_frame = ttk.Frame(dashboard_frame)
search_frame.pack(fill="x", pady=(0, 8))
ttk.Label(search_frame, text="Search logs:").pack(side="left", padx=(0, 8))
search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.pack(side="left", fill="x", expand=True)
search_var.trace_add("write", filter_logs)
ttk.Button(search_frame, text="Analyze Again", command=analyze_logs).pack(side="left", padx=8)

table_frame = ttk.Frame(dashboard_frame)
table_frame.pack(fill="both", expand=True)
columns = ("timestamp", "username", "ip", "status")
log_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
log_table.heading("timestamp", text="Timestamp")
log_table.heading("username", text="Username")
log_table.heading("ip", text="IP Address")
log_table.heading("status", text="Status")
log_table.column("timestamp", width=170)
log_table.column("username", width=130)
log_table.column("ip", width=150)
log_table.column("status", width=100)
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=log_table.yview)
log_table.configure(yscrollcommand=scrollbar.set)
log_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

ttk.Label(dashboard_frame, text="Suspicious Activity Alerts").pack(anchor="w", pady=(12, 4))
alert_text = tk.Text(dashboard_frame, height=3, bg="#fffaf3", fg="#8b2f20", font=("Consolas", 10), relief="solid", borderwidth=1)
alert_text.pack(fill="x")
alert_text.config(state="disabled")
status_label = ttk.Label(dashboard_frame, text="Sign in to begin.")
status_label.pack(anchor="w", pady=(8, 0))

username_entry.focus_set()
root.bind("<Return>", lambda event: login() if login_frame.winfo_ismapped() else None)
root.mainloop()
