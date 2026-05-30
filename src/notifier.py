import os
import requests

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")
        self.base_url = f"[https://api.telegram.org/bot](https://api.telegram.org/bot){self.token}/sendMessage"

        if not self.token or not self.chat_id:
            print("⚠️  [NOTIFIER WARNING] TELEGRAM_TOKEN or CHAT_ID missing in .env! Notifications disabled.")
        else:
            print("✅ [NOTIFIER] Ready: Telegram ChatOps integration initialized successfully.")

    def send_alert(self, detection_result: dict) -> bool:
        """Sends a structured security alert to the configured Telegram channel with network timeout safety."""
        if not self.token or not self.chat_id:
            return False

        message = (
            f"🚨 *CYBEKON INSIGHT SECURITY ALERT*\n"
            f"=================================\n"
            f"🔍 *Incident Rule:* `{detection_result['rule']}`\n"
            f"🌐 *Attacker IP:* `{detection_result['ip']}`\n"
            f"📋 *Raw Log Data:* \n`{detection_result['message']}`\n"
            f"=================================\n"
            f"🛡️ _Cybekon SOAR Active Response Module Triggered._"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(self.base_url, data=payload, timeout=5)

            if response.status_code == 429:
                print("⚠️  [NOTIFIER WARNING] Telegram API Rate Limit reached! Dropping alert to prevent crash.")
                return False

            if response.status_code != 200:
                print(f"[-] [NOTIFIER ERROR] Telegram API Error {response.status_code}: {response.text}")

            return response.status_code == 200

        except requests.exceptions.Timeout:
            print("[-] [NOTIFIER ERROR] Telegram API connection timed out. Skipping notification to save engine speed.")
            return False
        except Exception as e:
            print(f"[-] [NOTIFIER ERROR] Unexpected error while sending notification: {e}")
            return False