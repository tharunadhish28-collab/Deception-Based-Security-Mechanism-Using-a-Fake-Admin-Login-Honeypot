# Deception-Based-Security-Mechanism-Using-a-Fake-Admin-Login-Honeypot
Deception-Based Security Mechanism Using a Fake Admin Login Honeypot is a cybersecurity project built with Flask that simulates a fake admin login page to attract unauthorized users. The system records suspicious login attempts, logs activity, and demonstrates how deception techniques can be used as an additional layer of web application security.
# Deception-Based Security Mechanism Using a Fake Admin Login Honeypot

## Overview
This project is a **Flask-based cybersecurity application** that implements a **deception-based security mechanism** using a **fake admin login honeypot**.  
The purpose of this project is to detect suspicious or unauthorized login attempts by exposing a deceptive admin login page and monitoring attacker behavior.

The system acts as an additional layer of security by attracting malicious users to a fake login interface, recording their actions, and generating logs for analysis.

---

## Features
- Fake admin login page designed as a honeypot
- Detects suspicious login attempts
- Logs unauthorized access activity
- Captures attacker behavior for analysis
- Flask-based lightweight web application
- Demonstrates deception-based web security concepts

---

## Technologies Used
- **Python**
- **Flask**
- **HTML / CSS**
- **SQLite / File Logging** *(depending on your implementation)*

---

## Project Objective
The main objective of this project is to demonstrate how **deception technology** can improve web application security by:
- Identifying unauthorized users
- Monitoring suspicious login attempts
- Recording attack patterns
- Providing security logs for further investigation

---

## How It Works
1. A fake admin login page is exposed within the web application.
2. When an attacker or unauthorized user tries to access the page:
   - Their login attempt is captured
   - The entered credentials are logged
   - Additional request details (such as IP address, timestamp, or browser info) may be recorded
3. The system stores these details for security analysis.
4. This helps in identifying malicious behavior without exposing the real admin system.

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/deception-based-security-honeypot.git
cd deception-based-security-honeypot
