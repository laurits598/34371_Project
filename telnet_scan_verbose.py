#!/usr/bin/env python3
"""
telnet_check_verbose.py

Usage:
    python3 telnet_check_verbose.py targets.txt

Output:
    - results.csv (incrementally written)
    - prints live progress to stdout

Notes:
    - targets.txt: one host/IP per line (comments starting with # ignored)
    - Only probe hosts you own or have permission to test.
"""
import sys
import socket
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# -------- CONFIG --------
PORT = 23
TIMEOUT = 3.0         # seconds for connect/read
MAX_READ = 4096
WORKERS = 100         # concurrency
PROGRESS_UPDATE_EVERY = 1  # seconds (for ETA updates if many fast tasks)
RESULTS_CSV = "results.csv"
# ------------------------

lock = Lock()
stats_lock = Lock()
checked = 0
successes = 0
errors = 0
total = 0
start_time = None
running = True

def load_targets(path):
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            yield ln

def check_telnet(host, port=PORT, timeout=TIMEOUT):
    """Return (host, found_login_prompt_bool, banner_snippet, error_str)"""
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.settimeout(timeout)
        # provoke a prompt
        try:
            s.sendall(b"\r\n")
        except Exception:
            pass
        try:
            data = s.recv(MAX_READ)
        except Exception:
            data = b""
        try:
            s.close()
        except Exception:
            pass
        banner = data.decode("utf-8", errors="ignore").strip()
        low = banner.lower()
        is_login = ("login:" in low) or ("username:" in low) or ("password:" in low)
        # normalize banner for CSV (no newlines)
        banner_snip = banner.replace("\r", "\\r").replace("\n", "\\n")[:2000]
        return host, is_login, banner_snip, ""
    except (socket.timeout, ConnectionRefusedError) as e:
        return host, False, "", f"{type(e).__name__}"
    except Exception as e:
        return host, False, "", f"ERR:{e}"

def write_header_if_needed(path):
    try:
        # if file doesn't exist, create and write header
        with open(path, "a", newline="", encoding="utf-8") as csvf:
            pass
    except Exception:
        pass

def append_result_csv(path, row):
    with lock:
        with open(path, "a", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf)
            w.writerow(row)

def print_progress():
    global checked, successes, errors, total, start_time
    now = time.time()
    elapsed = now - start_time
    avg = elapsed / checked if checked else 0.0
    remain = total - checked
    eta = remain * avg
    # build one-line status
    status = (f"[{checked}/{total}] successes={successes} errors={errors} "
              f"avg={avg:.2f}s ETA={eta:.1f}s elapsed={elapsed:.1f}s")
    # overwrite previous line
    print("\r" + status.ljust(120), end="", flush=True)

def main(target_file):
    global checked, successes, errors, total, start_time

    targets = list(load_targets(target_file))
    total = len(targets)
    if total == 0:
        print("No targets found in", target_file)
        return

    # prepare CSV header if file empty
    # We'll open in append mode and write header if file size is zero
    import os
    header_needed = True
    if os.path.exists(RESULTS_CSV) and os.path.getsize(RESULTS_CSV) > 0:
        header_needed = False

    if header_needed:
        with open(RESULTS_CSV, "w", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf)
            w.writerow(["host", "telnet_prompt_found", "banner_snippet", "error"])

    start_time = time.time()
    last_progress = start_time

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = {ex.submit(check_telnet, t): t for t in targets}

        try:
            for fut in as_completed(futures):
                host = futures[fut]
                host, found, banner, err = fut.result()
                # update stats
                with stats_lock:
                    checked += 1
                    if err:
                        errors += 1
                    elif found:
                        successes += 1

                # write result row immediately
                append_result_csv(RESULTS_CSV, [host, str(found), banner, err])

                # print progress occasionally (or every result)
                now = time.time()
                if now - last_progress >= PROGRESS_UPDATE_EVERY or checked == total:
                    print_progress()
                    last_progress = now

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
        finally:
            # final progress line + newline
            print_progress()
            print("\nDone. Results appended to", RESULTS_CSV)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 telnet_check_verbose.py targets.txt")
        sys.exit(1)
    main(sys.argv[1])
