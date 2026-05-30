import sqlite3
import os
from datetime import datetime, timezone, timedelta


class SecurityDB:
    def __init__(self, db_folder="db", db_name="security_events.db"):
        self.db_folder = db_folder
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
            print(f"📁 Created directory: {self.db_folder}")

        self.db_path = os.path.join(self.db_folder, db_name)
        self.setup_db()

    def setup_db(self):
        """Creates the table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    rule_name TEXT,
                    ip_address TEXT,
                    message TEXT
                )
            ''')

    def save_alert(self, detection_result):
        """Saves the event to the database in ISO 8601 format."""
        utc_now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alerts (timestamp, rule_name, ip_address, message)
                VALUES (?, ?, ?, ?)
            ''', (utc_now, detection_result['rule'], detection_result['ip'], detection_result['message']))

    def get_ip_count(self, ip_address, minutes=5):
        """Counts alerts within the last X minutes using strict UTC synchronization."""
        time_threshold = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')

        query = "SELECT COUNT(*) FROM alerts WHERE ip_address = ? AND timestamp > ?"
        count = 0

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (ip_address, time_threshold))
                count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"[-] [DATABASE ERROR] Query Error: {e}")
            return 0