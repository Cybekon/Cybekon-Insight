import os
from dotenv import load_dotenv
from src.monitor import tail_file
from src.detector import DetectionEngine
from src.notifier import TelegramNotifier
from src.database import SecurityDB
from src.blocker import FirewallBlocker

load_dotenv()


def main():
    # Fetch configurations
    log_path = os.getenv("LOG_FILE_PATH")
    threshold = int(os.getenv("THRESHOLD", 5))

    print(f"--- 🛡️ Log-Based Detection & Security Monitor Started ---")
    print(f"--- 📂 Monitoring File: {log_path} ---")
    print(f"--- ⚙️ Security Threshold: {threshold} attempts ---")

    # Initialize professional modules
    db = SecurityDB()
    engine = DetectionEngine()
    notifier = TelegramNotifier()
    blocker = FirewallBlocker()

    # Track blocked IPs in this session to avoid redundant commands
    already_blocked_ips = set()

    try:
        # Start continuous monitoring
        for line in tail_file(log_path):
            # Step 1: Analyze the log line for threats
            result = engine.analyze(line)

            if result:
                ip = result['ip']

                if ip == "Unknown":
                    print(f"⚠️  [DETECTOR] Threat detected but Attacker IP could not be parsed. Line: {line}")
                    continue

                # Step 2: Save the event to the database (History/Logs)
                db.save_alert(result)

                # Step 3: Check how many times this IP has attacked in the last 5 minutes
                attack_count = db.get_ip_count(ip, minutes=5)

                print(f"🔍 [LOG] IP: {ip} | Attempt: {attack_count}/{threshold}")

                # Step 4: Decision Making (Logic)
                if attack_count >= threshold:
                    # Prevent redundant blocking and notifications
                    if ip not in already_blocked_ips:
                        # Upgrade the alert level
                        result['rule'] = f"🚨 BRUTE FORCE DETECTED ({attack_count} attempts)"

                        # Step 5: Active Response (Firewall Block)
                        block_status = blocker.block_ip(ip)

                        if block_status:
                            already_blocked_ips.add(ip)
                        else:
                            print(f"⚠️  [FIREWALL ERROR] Failed to apply block rule for IP: {ip}")

                        # Step 6: Send Notification
                        notif_status = notifier.send_alert(result)

                        if notif_status:
                            print(f"📱 ALERT: Critical threat notification sent for IP: {ip}")
                        else:
                            print(f"⚠️  ERROR: Failed to send Telegram notification.")
                    else:
                        print(f"ℹ️  [INFO] IP {ip} is already blocked. Skipping action.")

                # Optional: Initial warning
                elif attack_count == 1:
                    print(f"⚠️  WARNING: Initial threat detected from {ip}")

    except KeyboardInterrupt:
        print("\n👋 System shut down by user. Security monitoring terminated.")
    except Exception as e:
        print(f"\n❌ CRITICAL SYSTEM ERROR: {e}")


if __name__ == "__main__":
    main()