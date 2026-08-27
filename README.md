# Log Based Detection and Security Monitor
**Cybekon Insight** is a modular, high performance Intrusion Detection and Prevention System (IDS/IPS) designed for Linux servers. It monitors system logs in real time, identifies malicious patterns, logs threats to a database, and takes active defense measures by blocking attackers via system firewalls.

## 🚀 Key Features

* **Real time Log Tailing:** Continuously monitors log files without high CPU overhead.
* **Pattern Based Detection:** Uses advanced Regex to identify SSH brute-force, SQL Injection attempts, and unauthorized access.
* **Intelligent Thresholds:** Distinguishes between accidental mistyping and coordinated brute force attacks.
* **Persistent Database:** Stores every security event in a local SQLite database for forensic analysis.
* **Active Defense (IPS):** Automatically injects `iptables` rules to drop packets from verified attackers.
* **Instant Alerting:** Sends high priority security notifications to your phone via Telegram Bot API.

## 🏛️ Modular Architecture
The project is built on the **Separation of Concerns** principle:

* **`monitor.py`**: The "Eyes" - Handles low-level file reading.
* **`detector.py`**: The "Brain" - Analyzes patterns and determines threats.
* **`database.py`**: The "Memory" - Records history and tracks attack frequency.
* **`blocker.py`**: The "Shield" - Executes firewall commands to mitigate threats.
* **`notifier.py`**: The "Voice" - Communicates critical alerts to the admin.

## 🛠️ Installation & Setup

### 1. Requirements
* Python 3.10+
* Linux (Kali, Ubuntu, Debian, etc.) with `iptables`
* Root/Sudo privileges (for firewall blocking)

### 2. Clone and Prepare
```bash
# Clone the repository
git clone https://github.com/Cybekon/Cybekon-Insight.git
cd Cybekon-Insight

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
### 3. Configuration
Create a `.env` file in the project root directory and fill in your credentials (Check .env.example file)


**Note**: Make sure your bot has been started (click /start in Telegram) before running the script, otherwise the first notification might fail.

## ⚠️ Disclaimer

This tool is developed for **educational and ethical security monitoring purposes only**. 

* **Automated Blocking:** The automatic IP blocking feature modifies system firewall rules (`iptables`). Use it with caution, as improper configuration could lead to unintended service disruptions or self-lockouts.
* **Usage:** The developer is not responsible for any misuse, damage, or illegal activities caused by this software. 
* **Environment:** It is highly recommended to test this tool in a controlled lab environment before deploying it on production servers.

**Always ensure you have an alternative way to access your server (like a serial console or out-of-band management) when testing firewall automation.**