# ============================================================
# Deception-Based Security Mechanism with Honeypot Trap
# Educational Project - Flask Honeypot Demo
# ============================================================

from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

# In-memory dictionary to track suspicious attempts per IP
ip_attempt_counts = {}

LOG_FILE = "suspicious_logs.txt"
ALERT_THRESHOLD = 3  # Number of attempts before marking as "Potential Attacker"


# ─── Helper Functions ────────────────────────────────────────

def log_suspicious_activity(event_type, ip, details=""):
    """Write a suspicious event to the log file and print a terminal alert."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    severity = "HIGH" if is_potential_attacker(ip) else "WARNING"
    log_entry = (
        f"[{timestamp}] | SEVERITY: {severity} | EVENT: {event_type} | "
        f"IP: {ip} | DETAILS: {details}\n"
    )
    # Write to log file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    # Print alert to terminal
    print(f"\n{'='*60}")
    print(f"  🚨 HONEYPOT ALERT TRIGGERED")
    print(f"  {log_entry.strip()}")
    print(f"{'='*60}\n")


def increment_ip_attempt(ip):
    """Increment the suspicious attempt count for a given IP."""
    ip_attempt_counts[ip] = ip_attempt_counts.get(ip, 0) + 1


def is_potential_attacker(ip):
    """Return True if the IP has reached or exceeded the alert threshold."""
    return ip_attempt_counts.get(ip, 0) >= ALERT_THRESHOLD


# ─── Routes ──────────────────────────────────────────────────

@app.route("/")
def home():
    """Normal homepage — safe and visible to all users."""
    return """
    <html>
    <head><title>Home</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 80px; background: #f0f4f8; }
        h1 { color: #2c3e50; }
        p  { color: #555; font-size: 1.1em; }
    </style>
    </head>
    <body>
        <h1>Welcome to the Website</h1>
        <p>This is the normal public homepage. Nothing suspicious here.</p>
    </body>
    </html>
    """


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    """
    Honeypot route — looks like a real admin login but is entirely fake.
    Any access (GET or POST) is treated as suspicious.
    """
    ip = request.remote_addr

    if request.method == "GET":
        # Suspicious: someone discovered and visited the hidden page
        increment_ip_attempt(ip)
        log_suspicious_activity(
            event_type="Fake Admin Login Page Accessed",
            ip=ip,
            details=f"GET request to honeypot. Total attempts from this IP: {ip_attempt_counts[ip]}"
        )
        return render_template("admin_login.html")

    if request.method == "POST":
        # More suspicious: someone actually tried to log in
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        increment_ip_attempt(ip)
        log_suspicious_activity(
            event_type="Unauthorized Login Attempt on Honeypot",
            ip=ip,
            details=f"POST with username='{username}', password='{password}'. "
                    f"Total attempts: {ip_attempt_counts[ip]}"
        )

        # Escalated response for repeat offenders
        if is_potential_attacker(ip):
            return """
            <html>
            <head><title>Access Denied</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center;
                       padding: 80px; background: #1a1a2e; color: #e94560; }
                h2 { font-size: 2em; }
                p  { color: #aaa; font-size: 1.1em; }
            </style>
            </head>
            <body>
                <h2>⚠ Potential Attacker Detected</h2>
                <p>Your activity has been recorded and flagged for review.</p>
                <p>This incident has been logged with your IP address and timestamp.</p>
            </body>
            </html>
            """, 403

        # Standard response for first/second attempt
        return """
        <html>
        <head><title>Access Denied</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center;
                   padding: 80px; background: #f0f4f8; color: #c0392b; }
        </style>
        </head>
        <body>
            <h2>Access Denied</h2>
            <p>Invalid credentials. This attempt has been logged.</p>
        </body>
        </html>
        """, 401


@app.route("/view-logs")
def view_logs():
    """Display the contents of suspicious_logs.txt in the browser (demo only)."""
    try:
        with open(LOG_FILE, "r") as f:
            content = f.read() or "No suspicious activity logged yet."
    except FileNotFoundError:
        content = "Log file not found. No activity recorded yet."

    return f"""
    <html>
    <head><title>Suspicious Activity Logs</title>
    <style>
        body {{ font-family: monospace; background: #1e1e1e; color: #00ff88; padding: 30px; }}
        h2   {{ color: #ff4444; }}
        pre  {{ background: #111; padding: 20px; border-radius: 8px;
                border: 1px solid #333; white-space: pre-wrap; word-wrap: break-word; }}
    </style>
    </head>
    <body>
        <h2>🛡 Honeypot — Suspicious Activity Logs</h2>
        <pre>{content}</pre>
    </body>
    </html>
    """


# ─── Entry Point ─────────────────────────────────────────────

if __name__ == "__main__":
    # Create an empty log file if it doesn't exist
    open(LOG_FILE, "a").close()
    print("\n🛡  Honeypot server running at http://127.0.0.1:5000")
    print("   Fake admin page : http://127.0.0.1:5000/admin-login")
    print("   View logs       : http://127.0.0.1:5000/view-logs\n")
    app.run(debug=True)
