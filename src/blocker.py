import subprocess
import os

class FirewallBlocker:
    def __init__(self):
        # Control the OS
        self.is_linux = os.name != 'nt'

    def _is_already_blocked(self, ip_address: str) -> bool:
        """Checks whether the IP address is already blocked in iptables."""
        try:
            # We list the current rules using the `iptables -L INPUT -n` command
            check_command = ["sudo", "iptables", "-L", "INPUT", "-n"]
            result = subprocess.run(check_command, capture_output=True, text=True, check=True)

            # If this IP address appears in the output, it has already been blocked
            return ip_address in result.stdout
        except subprocess.CalledProcessError:
            # To err on the side of caution in cases of permission errors, etc., we return False
            return False

    def block_ip(self, ip_address: str) -> bool:
        """Adds a top priority DROP rule for the given IP address if not already blocked."""
        if not self.is_linux:
            print(f"[*] [FIREWALL] OS is not Linux. Simulating block for IP: {ip_address}")
            return True  # In the development environment (Windows), we return 'True' to prevent the flow from breaking

        # 1. Check: Prevent the addition of duplicate rules
        if self._is_already_blocked(ip_address):
            print(f"ℹ️  [FIREWALL] IP {ip_address} is already blocked in iptables. Skipping.")
            return True

        try:
            # 2. Solution: We move the rule to the very top (the first line) by using '-I' (Insert) instead of '-A'.
            # This ensures a strict block by bypassing all other permission rules.
            command = ["sudo", "iptables", "-I", "INPUT", "1", "-s", ip_address, "-j", "DROP"]

            subprocess.run(command, check=True, capture_output=True)
            print(f"🚫 [FIREWALL] Successfully blocked IP: {ip_address}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[-] [FIREWALL ERROR] Could not block {ip_address}. Error: {e.stderr.strip()}")
            return False
