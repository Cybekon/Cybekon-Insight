import time
import os


def tail_file(filename):
    # If there is no file, stay on standby at the system's helm instead of shutting down
    if not os.path.exists(filename):
        print(f"[*] [MONITOR] Waiting for log file to be created: {filename}")
        while not os.path.exists(filename):
            time.sleep(1)

    try:
        # We prevented it from crashing due to strange characters by adding encoding and error handling
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, os.SEEK_END)

            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # do not tire the processor
                    continue
                yield line.strip()  # Send after removing invisible spaces at the end of the line

    except PermissionError:
        print(f"[-] [ERROR] Permission denied for file: {filename}. Run as admin/root.")