#!/usr/bin/env python3
# telnet_check.py
# Usage: python3 telnet_check.py targets.txt
# targets.txt: one IP/hostname per line

import socket, sys, csv
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 3
PORT = 23
MAX_READ = 4096
WORKERS = 50

def check_telnet(host):
    """Return (host, open_boolean, banner_snippet)"""
    try:
        s = socket.create_connection((host, PORT), timeout=TIMEOUT)
        s.settimeout(TIMEOUT)
        # provoke a prompt
        try:
            s.sendall(b"\r\n")
        except Exception:
            pass
        try:
            data = s.recv(MAX_READ)
        except Exception:
            data = b""
        s.close()
        banner = data.decode("utf-8", errors="ignore").strip()
        is_login = "login:" in banner.lower() or "username:" in banner.lower()
        return host, is_login, banner.replace("\n", "\\n")[:1000]  # truncate/log-friendly
    except (socket.timeout, ConnectionRefusedError):
        return host, False, ""
    except Exception as e:
        return host, False, f"ERR:{e}"

def load_targets(path):
    with open(path, "r") as f:
        for line in f:
            h = line.strip()
            if h and not h.startswith("#"):
                yield h

def main(target_file):
    targets = list(load_targets(target_file))
    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = {ex.submit(check_telnet, t): t for t in targets}
        for fut in as_completed(futures):
            results.append(fut.result())

    # save CSV
    with open("results.csv", "w", newline="", encoding="utf-8") as csvf:
        w = csv.writer(csvf)
        w.writerow(["host","telnet_login_prompt","banner_snippet"])
        for host, found, banner in results:
            w.writerow([host, str(found), banner])

    print(f"Done: {len(results)} checked. Results -> results.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 telnet_check.py targets.txt")
        sys.exit(1)
    main(sys.argv[1])




'''
import socket, sys
host = "212.130.12.57" #"1.2.3.4"   # replace
port = 23
try:
    s = socket.create_connection((host, port), timeout=5)
    s.settimeout(5)
    s.sendall(b"\r\n")
    print(s.recv(8192).decode('utf-8', errors='ignore'))
except Exception as e:
    print("error:", e, file=sys.stderr)
finally:
    try: s.close()
    except: pass
'''