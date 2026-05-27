import re


class DetectionEngine:
    def __init__(self):
        self.rules = {
            # Linux Authentication: SSH failed password attempts
            "ssh_failed_password": r"Failed password for (?:invalid user )?\S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",

            # Linux Authentication: Login attempts with a non-existent username
            "invalid_user": r"Invalid user \S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",

            # Web Server (Nginx/Apache) Logs: SQL Injection Detection and IP Capture
            # In Nginx logs, the IP address is usually at the very beginning of the line (^).
            # We capture the IP address at the beginning of the line and search for the term “SQLi” in the rest of the line.
            "sql_injection_attempt": r"^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(?:UNION\s+SELECT|OR\s+'1'='1'|SELECT.*FROM|UNION\s+ALL\s+SELECT)",

            # Web Server Logs: Directory Traversal (Directory Traversal / Reading Sensitive Files)
            "directory_traversal": r"^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(?:\.\.\/|\.\.\\|/etc/passwd|/etc/shadow)"
        }

    def analyze(self, line):
        """It compares the log line against the rules and extracts threat data."""
        if not line:
            return None

        for rule_name, pattern in self.rules.items():
            try:
                # To remove case sensitivity in SQLi searches (re.IGNORECASE)
                # we run the rules using re.IGNORECASE (e.g., “union select” and “UNION SELECT” are treated as the same)
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    group_dict = match.groupdict()
                    ip_address = group_dict.get("ip", "Unknown")

                    return {
                        "rule": rule_name,
                        "ip": ip_address,
                        "message": line.strip()
                    }
            except re.error as e:
                print(f"[-] [REGEX ERROR] ({rule_name}): {e}")

        return None