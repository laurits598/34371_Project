import subprocess

TIMEOUT = "0.2"

def ping_ip(ip):
    result = subprocess.run(["ping", "-c", "1", "-W", TIMEOUT, ip], capture_output=True, text=True)
    output = result.stdout
    print(output)

    # Check for success in the summary line
    for line in output.splitlines():
        if "1 packets transmitted" in line and "1 received" in line and "0% packet loss" in line:
            return True
    return False



def check_http(ip):
    result = subprocess.run(["curl", "-m", TIMEOUT, "-I", f"http://{ip}/.htpasswd"], capture_output=True, text=True)
    #result = subprocess.run(["curl", "-m", TIMEOUT, "-I", f"http://{ip}/.htpasswd"], capture_output=True, text=True)

    output = result.stdout
    print(output)

    # Check for HTTP status code in the response headers
    for line in output.splitlines():
        if line.startswith("HTTP/"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                status_code = int(parts[1])
                if 200 <= status_code < 400:
                    return True
    return False


def test_ip(filename):
    active_ips = []

    with open(filename) as f:
        for i in range(0, 200):  # Limit to first 20 IPs for testing
            ip = f.readline().strip()
            if not ip:
                continue
            print(f"Pinging {ip}...")
            success = ping_ip(ip)

            if success:
                active_ips.append(ip)

            print(f"{ip} is {'reachable' if success else 'unreachable'}\n")

    print("\n" + "\n" + "#"*80 + "\n" + ">", len(active_ips), "active IPs:")
    for ip in active_ips:
        print(ip)
    print("\n" + "\n" + "#"*80 + "\n")
    return active_ips

def main():
    #test_ip("ips.txt")
    '''
    active_ips = test_ip()
    for ip in active_ips:
        print(f"curl {ip}...")
        success = check_http(ip)
        if success:
            print(f"{ip} has HTTP service\n")
    '''

    # Uncomment below to check HTTP service on active IPs
    with open("ips_port_80.txt") as f:
        for line in f:
            ip = line.strip()
            if not ip:
                continue  # Skip empty lines
            #print(f"curl {ip}...")
            success = check_http(ip)
            if success:
                print(f"{ip} has HTTP service\n")


if __name__ == "__main__":
    main()


