import subprocess

TIMEOUT = "0.15"  # Consider increasing to 1 for reliability

def check_http(ip, only_200=True):
    try:
        result = subprocess.run(
            #["curl", "-m", TIMEOUT, "-I", f"http://{ip}/.htpasswd"],
            ["curl", "-m", TIMEOUT, "-I", f"http://{ip}/files"],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr  # Include stderr for diagnostics

        for line in output.splitlines():
            if line.startswith("HTTP/"):
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    status_code = int(parts[1])
                    if only_200:
                        return status_code == 200
                    else:
                        return 200 <= status_code < 400
    except Exception as e:
        print(f"Error checking HTTP on {ip}: {e}")
    return False

def pretty_print(ip, message="HTTP 200 OK", pad=20):
    spacing = pad - len(ip)
    print(f"[{ip}]:{' ' * spacing}{message}")

def main():
    with open("ips_port_80.txt") as f:
        for line in f:
            ip = line.strip()
            if not ip:
                continue
            if check_http(ip, only_200=True):  # Change to False to allow all 2xx/3xx
                pretty_print(ip)

if __name__ == "__main__":
    main()